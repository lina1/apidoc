Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/SolutionsCloud/apidoc/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

ApiDoc could always use more documentation, whether as part of the
official ApiDoc docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/SolutionsCloud/apidoc/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)


Setting Up the Code for Local Development
-----------------------------------------

Here's how to set up `ApiDoc` for local development.

1. Fork the `ApiDoc` repo on GitHub.
2. Clone your fork locally

.. code-block:: console

    $ git clone git@github.com:your_name_here/apidoc.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development

.. code-block:: console

    $ mkvirtualenv apidoc
    $ cd apidoc/
    $ pip install -e .[contribute]


4. Create a branch for local development

.. code-block:: console

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests and flake8

.. code-block:: console

    $ flake8 --show-source --ignore=E501 --statistics .
    $ python setup.py test

6. Commit your changes and push your branch to GitHub

.. code-block:: console

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Check that the test coverage hasn't dropped

.. code-block:: console

    $ behave --format progress2 tests/features/
    $ coverage3 run --branch --source apidoc setup.py test
    $ coverage3 report -m

8. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.2, 3.3. Check
   https://travis-ci.org/SolutionsCloud/apidoc/pull_requests and make sure that
   the tests pass for all supported Python versions.

Tips
----

To run a particular test

.. code-block:: console

    $ python -m unittest tests.test_find.TestFind.test_find_template

To run a subset of tests

.. code-block:: console

    $ python -m unittest tests.test_find