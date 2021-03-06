from app.helpers import (
    format_for_table,
    get_average_test_runs,
    get_last_test_run_per_release,
    get_latest_releases,
    get_test_runs
)
from app.models import Release
from flask import render_template
from flask import Blueprint


release_blueprint = Blueprint(
    'release', __name__,
    template_folder='templates'
)


@release_blueprint.route('/releases/', methods=['GET', ])
def index():
    releases = get_latest_releases()
    return render_template('releases.html', rows=releases)


@release_blueprint.route('/releases/<minor>', methods=['GET', ])
def minor(minor):
    dataset = []

    releases = Release.query.filter_by(
        minor=minor
    ).order_by(
        Release.patch.desc(),
    ).all()

    for release in releases:
        test_runs = get_last_test_run_per_release(release)
        for test_run in test_runs:
            dataset.append(test_run)

    return render_template('minor_releases.html', test_runs=dataset)


@release_blueprint.route('/release/<int:id>', methods=['GET', ])
def release(id):
    release = Release.query.filter_by(id=id).first()
    tc_fields = [
        'name',
        'passed',
        'failed',
        'skipped',
        'error'
    ]
    pass_fail_fields = [
        'name',
        'percent_passed',
        'percent_failed',
    ]
    execution_fields = [
        'name',
        'percent_executed',
        'percent_not_executed'
    ]
    test_runs = get_test_runs(release=release)

    avg_runs = get_average_test_runs(release=release)
    tc_data = format_for_table(avg_runs, tc_fields)
    passfail_data = format_for_table(avg_runs, pass_fail_fields)
    execution_data = format_for_table(avg_runs, execution_fields)

    return render_template(
        'release.html',
        testcase=tc_data,
        passfail=passfail_data,
        execution=execution_data,
        release=release,
        rows=test_runs)
