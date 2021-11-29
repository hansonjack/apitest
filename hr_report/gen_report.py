import io
import os
from datetime import datetime
from httprunner.utils import get_platform, ExtendJSONEncoder
from jinja2 import Template
from loguru import logger


def handle_summary(data):
    summary = {
        "success": True,
        "stat": {
            "testcases": {"total": 0, "success": 0, "fail": 0},
            "teststeps": {"total": 0, "failures": 0, "successes": 0},
        },
        "time": {"start_at": data['time']['start_at'], "duration": data['time']['duration']},
        "platform": get_platform(),
        "details": [],
    }

    for item in data['step_datas']:
        summary["success"] &= item['success']

        summary["stat"]["testcases"]["total"] += 1
        summary["stat"]["teststeps"]["total"] += len(item)
        if item['success']:
            summary["stat"]["testcases"]["success"] += 1
            summary["stat"]["teststeps"]["successes"] += len(
                item
            )
        else:
            summary["stat"]["testcases"]["fail"] += 1
            summary["stat"]["teststeps"]["successes"] += (
                len(item) - 1
            )
            summary["stat"]["teststeps"]["failures"] += 1

        testcase_summary_json = item
        testcase_summary_json["records"] = testcase_summary_json.pop("data")
        summary["details"].append(testcase_summary_json)
        summary.pop('stat')
        return summary

def gen_html_report(summary, report_template=None, report_dir=None, report_file=None):
    """ render html report with specified report name and template
    Args:
        summary (dict): test result summary data
        report_template (str): specify html report template path, template should be in Jinja2 format.
        report_dir (str): specify html report save directory
        report_file (str): specify html report file path, this has higher priority than specifying report dir.
    """
    if not summary["time"]:
        logger.info("test result summary is empty ! {}".format(summary))
        return

    if not report_template:
        report_template = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "template.html"
        )
        logger.info("No html report template specified, use default.")
    else:
        logger.info("render with html report template: {}".format(report_template))

    logger.info("Start to render Html report ...")

    start_at_timestamp = summary["time"]["start_at"]
    utc_time_iso_8601_str = datetime.utcfromtimestamp(start_at_timestamp).isoformat()
    summary["time"]["start_datetime"] = utc_time_iso_8601_str

    if report_file:
        report_dir = os.path.dirname(report_file)
        report_file_name = os.path.basename(report_file)
    else:
        report_dir = report_dir or os.path.join(os.getcwd(), "reports")
        # fix #826: Windows does not support file name include ":"
        report_file_name = "{}.html".format(utc_time_iso_8601_str.replace(":", "").replace("-", ""))

    if not os.path.isdir(report_dir):
        os.makedirs(report_dir)
    print(report_template)
    report_path = os.path.join(report_dir, report_file_name)
    with io.open(report_template, "r", encoding='utf-8') as fp_r:
        template_content = fp_r.read()
        # print(template_content)
        with io.open(report_path, 'w', encoding='utf-8') as fp_w:
            rendered_content = Template(
                template_content,
                extensions=["jinja2.ext.loopcontrols"]
            ).render(summary)
            fp_w.write(rendered_content)

    logger.info("Generated Html report: {}".format(report_path))