import pytest

import degrees

def test_multiple_paths_small(capsys):
    input_values = ['Kevin Bacon', 'Sally Field']

    def mock_input(s):
        print(s, end='')
        return input_values.pop(0)

    degrees.input = mock_input

    # this is a hack that should really be avoided. best to keep global vars inside functions or classes
    degrees.names = {}
    degrees.people = {}
    degrees.movies = {}
    degrees.main('small')

    out, err = capsys.readouterr()
    possible_path_1 = '\n'.join([
        'Loading data...', 'Data loaded.',
        'Name: Name: ' + '2 degrees of separation.',
        '1: Kevin Bacon and Tom Hanks starred in Apollo 13',
        '2: Tom Hanks and Sally Field starred in Forrest Gump\n'
    ])
    possible_path_2 = '\n'.join([
        'Loading data...', 'Data loaded.',
        'Name: Name: ' + '2 degrees of separation.',
        '1: Kevin Bacon and Gary Sinise starred in Apollo 13',
        '2: Gary Sinise and Sally Field starred in Forrest Gump\n'
    ])

    assert (out == possible_path_1) | (out == possible_path_2)
    assert err == ''


@pytest.mark.parametrize('directory', ['small', 'large'])
def test_same_actor(capsys, directory):
    input_values = ['Tom Hanks', 'Tom Hanks']

    def mock_input(s):
        print(s, end='')
        return input_values.pop(0)

    degrees.input = mock_input
    # this is a hack that should really be avoided. best to keep global vars inside functions or classes
    degrees.names = {}
    degrees.people = {}
    degrees.movies = {}
    degrees.main(directory)

    out, err = capsys.readouterr()
    expected_output = '\n'.join([
        'Loading data...', 'Data loaded.',
        'Name: Name: ' + '0 degrees of separation.\n'
    ])
    assert (out == expected_output)
    assert err == ''


def test_no_connection_small(capsys):
    input_values = ['Kevin Bacon', 'Emma Watson']

    def mock_input(s):
        print(s, end='')
        return input_values.pop(0)

    degrees.input = mock_input
    # this is a hack that should really be avoided. best to keep global vars inside functions or classes
    degrees.names = {}
    degrees.people = {}
    degrees.movies = {}
    degrees.main('small')

    out, err = capsys.readouterr()
    expected_output = '\n'.join([
        'Loading data...', 'Data loaded.', 'Name: Name: ' + 'Not connected.\n'
    ])
    assert (out == expected_output)
    assert err == ''


@pytest.mark.parametrize('directory', ['small', 'large'])
def test_co_starred(capsys, directory):
    input_values = ['Tom Cruise', 'Jack Nicholson']

    def mock_input(s):
        print(s, end='')
        return input_values.pop(0)

    degrees.input = mock_input
    # this is a hack that should really be avoided. best to keep global vars inside functions or classes
    degrees.names = {}
    degrees.people = {}
    degrees.movies = {}
    degrees.main(directory)

    out, err = capsys.readouterr()
    expected_output = '\n'.join([
        'Loading data...', 'Data loaded.',
        'Name: Name: ' + '1 degrees of separation.',
        '1: Tom Cruise and Jack Nicholson starred in A Few Good Men\n'
    ])
    assert (out == expected_output)
    assert err == ''


@pytest.mark.parametrize('directory', ['small', 'large'])
def test_degree_multiple_runs(capsys, directory):
    def run():
        input_values = ['Dustin Hoffman', 'Robin Wright']

        def mock_input(s):
            print(s, end='')
            return input_values.pop(0)

        degrees.input = mock_input
        # this is a hack that should really be avoided. best to keep global vars inside functions or classes
        degrees.names = {}
        degrees.people = {}
        degrees.movies = {}
        degrees.main(directory)

        out, err = capsys.readouterr()
        return out, err

    # first run
    out1, err1 = run()
    degrees1 = out1.split('\n')[2].split('Name: Name: ')[1]

    # second run
    out2, err2 = run()
    degrees2 = out2.split('\n')[2].split('Name: Name: ')[1]

    assert (degrees1 == degrees2)
    assert (err1 == '') & (err2 == '')