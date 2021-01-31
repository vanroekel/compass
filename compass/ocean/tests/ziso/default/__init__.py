from compass.testcase import set_testcase_subdir, add_step, run_steps
from compass.namelist import add_namelist_file
from compass.ocean.tests.ziso import initial_state, forward
from compass.ocean.tests import ziso
from compass.validate import compare_variables, compare_timers


def collect(testcase):
    """
    Update the dictionary of test case properties and add steps

    Parameters
    ----------
    testcase : dict
        A dictionary of properties of this test case, which can be updated
    """
    resolution = testcase['resolution']
    testcase['description'] = 'Zonally periodic Idealized Southern Ocean '\
                              '(ZISO) {} default test'.format(resolution)

    module = __name__

    res_params = {'20km': {'cores': 4, 'min_cores': 2,
                           'max_memory': 1000, 'max_disk': 1000}}

    if resolution not in res_params:
        raise ValueError('Unsupported resolution {}. Supported values are: '
                         '{}'.format(resolution, list(res_params)))

    res_params = res_params[resolution]

    subdir = '{}/{}'.format(resolution, testcase['name'])
    set_testcase_subdir(testcase, subdir)

    add_step(testcase, initial_state, resolution=resolution, with_frazil=False)

    step = add_step(testcase, forward, resolution=resolution,
                    cores=res_params['cores'],
                    min_cores=res_params['min_cores'],
                    max_memory=res_params['max_memory'],
                    max_disk=res_params['max_disk'], with_analysis=True,
                    with_frazil=False)
    if resolution == '20km':
        # particles are on only for the 20km test case
        add_namelist_file(step, module,
                          'namelist.{}.forward'.format(resolution))


def configure(testcase, config):
    """
    Modify the configuration options for this test case

    Parameters
    ----------
    testcase : dict
        A dictionary of properties of this test case

    config : configparser.ConfigParser
        Configuration options for this test case
    """
    ziso.configure(testcase, config)


def run(testcase, test_suite, config, logger):
    """
    Run each step of the testcase

    Parameters
    ----------
    testcase : dict
        A dictionary of properties of this test case

    test_suite : dict
        A dictionary of properties of the test suite

    config : configparser.ConfigParser
        Configuration options for this test case

    logger : logging.Logger
        A logger for output from the test case
    """
    work_dir = testcase['work_dir']
    run_steps(testcase, test_suite, config, logger)

    steps = testcase['steps_to_run']
    if 'forward' in steps:
        variables = ['temperature', 'layerThickness']
        compare_variables(
            variables, config, work_dir,
            filename1='forward/output/output.0001-01-01_00.00.00.nc')

        variables = ['xParticle', 'yParticle', 'zParticle', 'zLevelParticle',
                     'buoyancyParticle', 'indexToParticleID', 'currentCell',
                     'transfered', 'numTimesReset']
        compare_variables(variables, config, work_dir,
                          filename1='forward/analysis_members/'
                                    'lagrPartTrack.0001-01-01_00.00.00.nc')

        timers = ['init_lagrPartTrack', 'compute_lagrPartTrack',
                  'write_lagrPartTrack', 'restart_lagrPartTrack',
                  'finalize_lagrPartTrack']
        compare_timers(timers, config, work_dir, rundir1='forward')
