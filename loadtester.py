import glob
import os
from pprint import pprint

import yaml
from locust import HttpLocust, TaskSet, between


def load_rules():
    dir_rules = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rules')
    if os.path.exists(dir_rules):
        pattern = f'{dir_rules}/*.yaml'
        for each in glob.glob(pattern):
            if not os.path.exists(each):
                continue
            try:
                result = None
                with open(each) as tmpf:
                    result = yaml.safe_load(tmpf)
                yield  result
            except Exception as exc:
                print(exc)
    else:
        print('No rules directory found.')


def generate_task(payload):
    endpoint = payload.get('endpoint')
    http_method = payload.get('method').lower()
    headers= payload.get('headers')
    data = payload.get('data')
    return lambda l: getattr(l.client, http_method)(endpoint,
                                                    headers=headers,
                                                    data=data)


def create_taskset():
    """Create Taskset class.

    NOTE: currently, single host is only supported.

    Returns:
        HttpLocust -- Locust class
    """
    rules = load_rules()
    # taskset_classes = []
    for e, each_rule in enumerate(rules):
        # pprint(each_rule)
        class_name = each_rule.get('name') or f'UserClass{e}'
        host = '{proto}://{host}:{port}'.format(**each_rule)
        # print(host)
        tasks = each_rule.get('tasks')
        fn_tasks = [generate_task(each_task) for each_task in tasks]
        new_class = type(class_name, (TaskSet, ), dict(tasks=fn_tasks))
        # help(new_class)
        # taskset_classes.append(new_class)

        locust_runner = type('LoadTester',
                                (HttpLocust,),
                                dict(
                                    host=host,
                                    task_set=new_class,
                                    wait_time=between(2, 5)))
        # help(locust_runner)
        return locust_runner


load_tester = create_taskset()
