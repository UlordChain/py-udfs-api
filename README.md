# py-udfs-api

[![](https://img.shields.io/badge/project-udfs-blue.svg?style=flat-square)](https://udfs.io/)
[![](https://img.shields.io/badge/freenode-%23udfs-blue.svg?style=flat-square)](https://webchat.freenode.net/?channels=%23udfs)
[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![](https://img.shields.io/pypi/v/udfsapi.svg?style=flat-square)](https://pypi.python.org/pypi/udfsapi)
[![Build Status](https://travis-ci.org/udfs/py-udfs-api.svg?branch=master)](https://travis-ci.org/udfs/py-udfs-api)

![Python udfs HTTP Client Library](https://udfs.io/udfs/QmQJ68PFMDdAsgCZvA1UVzzn18asVcf7HVvCDgpjiSCAse)

Check out [the client API reference](https://udfs.io/ipns/QmZ86ow1byeyhNRJEatWxGPJKcnQKG7s51MtbHdxxUddTH/Software/Python/udfsapi/) for the full command reference.

**Important:** The `py-udfs-api` PIP package and Python module have both been renamed to `udfsapi` (no dash, lower-case `a`).
The legacy `udfs-api`/`udfsApi` package/module will only work for udfs 0.3.x and Python 2 and is deprecated. [Please upgrade](#important-changes-from-udfsapi-02x)!

**Note:** This library constantly has to change to stay compatible with the udfs HTTP API.
Currently, this library is tested against [go-udfs v0.4.10](https://github.com/udfs/go-udfs/releases/tag/v0.4.10).
You may experience compatibility issues when attempting to use it with other versions of go-udfs.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Documentation](#documentation)
  - [Important changes from udfsApi 0.2.x](#important-changes-from-udfsapi-02x)
- [Featured Projects](#featured-projects)
- [Contribute](#contribute)
  - [IRC](#irc)
  - [Bug reports](#bug-reports)
  - [Pull requests](#pull-requests)
- [License](#license)

## Install

Install with pip:

```sh
pip install udfsapi
```

## Usage

Basic use-case (requires a running instance of udfs daemon):

```py
>>> import udfsapi
>>> api = udfsapi.connect('127.0.0.1', 5001)
>>> res = api.add('test.txt')
>>> res
{'Hash': 'QmWxS5aNTFEc9XbMX1ASvLET1zrqEaTssqt33rVZQCQb22', 'Name': 'test.txt'}
>>> api.cat(res['Hash'])
'fdsafkljdskafjaksdjf\n'
```

Administrative functions:

```py
>>> api.id()
{'Addresses': ['/ip4/127.0.0.1/tcp/4001/udfs/QmS2C4MjZsv2iP1UDMMLCYqJ4WeJw8n3vXx1VKxW1UbqHS',
               '/ip6/::1/tcp/4001/udfs/QmS2C4MjZsv2iP1UDMMLCYqJ4WeJw8n3vXx1VKxW1UbqHS'],
 'AgentVersion': 'go-udfs/0.4.10',
 'ID': 'QmS2C4MjZsv2iP1UDMMLCYqJ4WeJw8n3vXx1VKxW1UbqHS',
 'ProtocolVersion': 'udfs/0.1.0',
 'PublicKey': 'CAASpgIwgg ... 3FcjAgMBAAE='}
```

Pass in API options:

```py
>>> api.pin_ls(type='all')
{'Keys': {'QmNMELyizsfFdNZW3yKTi1SE2pErifwDTXx6vvQBfwcJbU': {'Count': 1,
                                                             'Type': 'indirect'},
          'QmNQ1h6o1xJARvYzwmySPsuv9L5XfzS4WTvJSTAWwYRSd8': {'Count': 1,
                                                             'Type': 'indirect'},
          …
```

Add a directory and match against a filename pattern:

```py
>>> api.add('photos', match='*.jpg')
[{'Hash': 'QmcqBstfu5AWpXUqbucwimmWdJbu89qqYmE3WXVktvaXhX',
  'Name': 'photos/photo1.jpg'},
 {'Hash': 'QmSbmgg7kYwkSNzGLvWELnw1KthvTAMszN5TNg3XQ799Fu',
  'Name': 'photos/photo2.jpg'},
 {'Hash': 'Qma6K85PJ8dN3qWjxgsDNaMjWjTNy8ygUWXH2kfoq9bVxH',
  'Name': 'photos/photo3.jpg'}]
```

Or add a directory recursively:

```py
>>> api.add('fake_dir', recursive=True)
[{'Hash': 'QmQcCtMgLVwvMQGu6mvsRYLjwqrZJcYtH4mboM9urWW9vX',
  'Name': 'fake_dir/fsdfgh'},
 {'Hash': 'QmNuvmuFeeWWpxjCQwLkHshr8iqhGLWXFzSGzafBeawTTZ',
  'Name': 'fake_dir/test2/llllg'},
 {'Hash': 'QmX1dd5DtkgoiYRKaPQPTCtXArUu4jEZ62rJBUcd5WhxAZ',
  'Name': 'fake_dir/test2'},
 {'Hash': 'Qmenzb5J4fR9c69BbpbBhPTSp2Snjthu2hKPWGPPJUHb9M',
  'Name': 'fake_dir'}]
```

This module also contains some helper functions for adding strings and JSON to udfs:

```py
>>> lst = [1, 77, 'lol']
>>> client.add_json(lst)
'QmQ4R5cCUYBWiJpNL7mFe4LDrwD6qBr5Re17BoRAY9VNpd'
>>> client.get_json(_)
[1, 77, 'lol']
```

## Documentation

Documentation (currently mostly API documentation unfortunately) is available on udfs:

https://udfs.io/ipns/QmZ86ow1byeyhNRJEatWxGPJKcnQKG7s51MtbHdxxUddTH/Software/Python/udfsapi/

The `udfs` [command-line Client documentation](https://udfs.io/docs/commands/) may also be useful in some cases.

### Important changes from `udfsApi 0.2.x`

 * The Python package has been renamed from `udfsApi` to `udfsapi`
 * The PIP module has been renamed from `udfs-api` to `udfsapi` (please update your requirement files)
 * A lot of changes in the internal code
    - Commands have been completely removed
    - Usage of `requests` or other libraries is considered an implementation detail from now on
 * Most parts of the library (except for `Client()`) are now considered internal and may therefore break at any time
   ([reference](https://udfs.io/ipns/QmZ86ow1byeyhNRJEatWxGPJKcnQKG7s51MtbHdxxUddTH/Software/Python/udfsapi/internal_ref.html))
    - We will try to keep breakage for these modules at a minimum
    - If you require stabilisation of some feature please open an issue with the feature in question and your preceived use-case
 * Raised exceptions have been completely changed and are now documented with guaranteed backwards compatibility
   ([reference](https://udfs.io/ipns/QmZ86ow1byeyhNRJEatWxGPJKcnQKG7s51MtbHdxxUddTH/Software/Python/udfsapi/api_ref.html#module-udfsapi.exceptions))
 * The new `udfsapi.connect()` function allows creating a `Client` instance, while also checking whether a compatible udfs daemon instance is actually available
 * Methods in `Client()` now have parameters for options

## Featured Projects

Projects that currently use py-udfs-api. If your project isn't here, feel free to submit a PR to add it!

- [git-remote-udfs](https://github.com/larsks/git-remote-udfs) allows users to push and pull git repositories from the udfs network.
- [InterPlanetary Wayback](https://github.com/oduwsdl/ipwb) interfaces web archive ([WARC](https://www.iso.org/standard/44717.html)) files for distributed indexing and replay using udfs.

## Contribute

### IRC

Join us on IRC at `#udfs` on [chat.freenode.net](https://webchat.freenode.net) if you have any suggestions or questions,
or if you just want to discuss udfs and python.

### Bug reports

You can submit bug reports using the [GitHub issue tracker](https://github.com/udfs/python-udfs-api/issues).

### Pull requests

Pull requests are welcome.  Before submitting a new pull request, please
make sure that your code passes both the [code formatting](https://www.python.org/dev/peps/pep-0008/) check:

    $ tox -e codestyle

And the unit tests:

    $ tox

You can arrange to run the code style tests automatically before each commit by
installing a `pre-commit` hook:

    $ ./tools/pre-commit --install

Please make sure to include new unit tests for new features or changes in
behavior.

## License

This code is distributed under the terms of the [MIT license](https://opensource.org/licenses/MIT).  Details can be found in the file
[LICENSE](LICENSE) in this repository.
