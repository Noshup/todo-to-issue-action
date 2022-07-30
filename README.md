# Comment to Issue Action

### ATTENTION: This is a Fork of alstr's [todo-to-issue-action](https://github.com/alstr/todo-to-issue-action)! This implementation would not have been possible without their hard work. I have simply extended its functionality a little bit.

This action will convert newly committed comments to GitHub issues on push. It will also optionally close the issues if the TODOs are removed in a future commit. Works with almost any programming language.

As stated above, this action is a modified version of the Todo-To-Issue-Action. The following features have been added/changed:

- Workflow inputs 'LABEL', 'PROJECT_SECRET', 'USER_PROJECTS' have been removed and manual project association logic has been deleted from the action entirely as the new GitHub projects' Beta is incompatible with that implementation, and 'LABEL' is being replaced by 'ISSUE_IDENTIFIERS'.
- Using the workflow input 'ISSUE_IDENTIFIERS', you can select which terms will be used to determine whether a comment in your code will be extracted as an Issue. By default, 'TODO' is the only term which is matched with lines in your commits' difference files. The input param is of type String, and should be structured like so: 'TERM|TERMB|TERMC|TERMD'. Do not add the pipe operator if you only have one term.
- Issues are not automatically created with the TODO label attached anymore. The identifying term has no bearing on the issue labeling, so you will want to make sure you use the labels property in your multiline comments.
- An additional Github API service has been added. This supports custom code snippets attached to your generated issues. The previous implementation only supported code snippets which were taken from the difference file, which could be somewhat limiting. Now, you can specify which lines of code the snippet should cover (if not specified, defaults back to diff-based snippet) and the API service will query GitHub for the source code file in which the comment is located, then parse the content to match the indicated line numbers. This means the GitHub token you provide should have API permissions!

## Usage

Simply add a comment starting with TODO, followed by a colon and/or space. Here's an example for Python that creates an issue named after the TODO:

```python
    def hello_world():
        # TODO Come up with a more imaginative greeting
        print('Hello world!')
```

Multiline TODOs are supported, with additional lines inserted into the issue body. A range of options can also be provided to apply to the new issue:

```python
    def hello_world():
        # TODO Come up with a more imaginative greeting
        #  Everyone uses hello world and it's boring.
        #  labels: enhancement, help wanted
        #  assignees: alstr, bouteillerAlan, hbjydev
        #  milestone: 1
        #  lines: 25,55
        print('Hello world!')
```

## Setup

Create a `workflow.yml` file in your `.github/workflows` directory like:

```yml
    name: "Workflow"
    on: ["push"]
    jobs:
      build:
        runs-on: "ubuntu-latest"
        steps:
          - uses: "actions/checkout@master"
          - name: "Comment to Issue"
            uses: "Noshup/todo-to-issue-action@master"
            id: "todo"
```

See [Github's workflow syntax](https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions) for further details on this file.

The workflow file takes the following optional inputs:

| Input            | Required | Description                                                                                                                                                                                                  |
|------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `TOKEN`          | No | The GitHub access token to allow us to retrieve, create and update issues for your repo. Default: `${{ github.token }}`.                                                                                     |
| `ISSUE_IDENTIFIERS` | No | The Tag used to signify that a comment is/to be associated with an issue in Github. Default value is 'TODO', but you can add as many terms as you like, separating each term using the pipe operator. For example: `'TODO|BUG|TESTING'`                                     |
| `CLOSE_ISSUES`   | No | Optional boolean input that specifies whether to attempt to close an issue when a TODO is removed. Default: `true`.                                                                                          |
| `AUTO_P`         | No | Optional boolean input that specifies whether to format each line in multiline TODOs as a new paragraph. Default: `true`.                                                                                    |
| `IGNORE`         | No | Optional string input that provides comma-delimited regular expressions that match files in the repo that we should not scan for TODOs. By default, we will scan all files.                                  |
| `AUTO_ASSIGN`    | No | Optional boolean input that specifies whether to assign the newly created issue to the user who triggered the action. If users are manually assigned to an issue, this setting is ignored. Default: `false`. |
| `ISSUE_TEMPLATE` | No | You can override the default issue template by providing your own here. Markdown is supported, and you can inject the issue title, body, code URL and snippet. Example: `"This is my issue title: **{{ title }}**\n\nThis is my issue body: **{{ body }}**\n\nThis is my code URL: **{{ url }}**\n\nThis is my snippet:\n\n{{ snippet }}"`                                     |

These can be specified in `with` in the workflow file.

There are additional inputs if you want to be able to assign issues to projects. Consult the relevant section below for more details.

### Considerations

* TODOs are found by analysing the difference between the new commit and its previous one (i.e., the diff). That means that if this action is implemented during development, any existing TODOs will not be detected. For them to be detected, you would have to remove them, commit, put them back, and commit again.
* Should you change the TODO text, this will currently create a new issue.
* Closing TODOs is still somewhat experimental.

## Supported Languages

* ABAP
* ABAP CDS
* AutoHotkey
* C
* C++
* C#
* CSS
* Crystal
* Dart
* Elixir
* Go
* Handlebars
* HCL
* Haskell
* HTML
* Java
* JavaScript
* Julia
* Kotlin
* Less
* Markdown
* Objective-C
* Org Mode
* PHP
* Python
* R
* Razor
* Ruby
* Rust
* Sass
* Scala
* SCSS
* Shell
* SQL
* Swift
* TeX
* TSX
* Twig
* TypeScript
* Vue
* YAML

New languages can easily be added to the `syntax.json` file used by the action to identify tagged comments. When adding languages, follow the structure of existing entries, and use the language name defined by GitHub in [`languages.yml`](https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml). PRs adding new languages are welcome and appreciated. Please add a test for your language in order for your PR to be accepted. 

## Comment Options

Unless specified otherwise, options should be on their own line, below the initial TODO (or other identifying) declaration.

### `assignees:`

Comma-separated list of usernames to assign to the issue.

### `labels:`

Comma-separated list of labels to add to the issue. If any of the labels do not already exist, they will be created. The `todo` label is no longer automatically added to issues; you must instead add this label yourself.

### `milestone:`

Milestone ID to assign to the issue. Only a single milestone can be specified and this must already have been created.

### `lines:`

Line Numbers to specify the exact contents of the Code Snippet which will be attached to the Issue in GitHub. These should be comma-separated with no spaces, e.g. `lines: 16,98` and will be used on the same source file in which the comment exists. If you omit this property, the action will instead follow the same routine as alstr's original version; the snippet will be created using the difference file. 

## Troubleshooting

### No issues have been created

Make sure your file language is in `syntax.json`. Also, the action will not recognise existing TODOs that have already been pushed.

If a similar TODO appears in the diff as both an addition and deletion, it is assumed to have been moved, so is ignored.

In case, your workflow is executed but no issue is generated, check if you have given permissions to Workflows. Go to your GitHub Project, Settings->Actions(General)->Workflow permissions and Enable "Read and write permissions".

### Multiple issues have been created

Issues are created whenever the action runs and finds a newly added TODO in the diff. Rebasing may cause a TODO to show up in a diff multiple times. This is an acknowledged issue, but you may have some luck by adjusting your workflow file.

## Contributing & Issues

If you do encounter any problems, please file an issue or submit a PR. Everyone is welcome and encouraged to contribute.

## Running tests locally 

To run the tests locally, simply run the following in the main repo:
```shell
python -m unittest
```

## Customising

If you want to fork this action to customise its behaviour, there are a few steps you should take to ensure your changes run:

* In `workflow.yml`, set `uses: ` to your action.
* In `action.yml`, set `image: ` to `Dockerfile`, rather than the prebuilt image.
* If customising `syntax.json`, you will want to update the URL in `main.py` to target your version of the file.

## Thanks

The action was developed for the GitHub Hackathon. Whilst every effort is made to ensure it works, it comes with no guarantee.

Thanks to all those who have [contributed](https://github.com/alstr/todo-to-issue-action/graphs/contributors) to the further development of this action's source repo.

Thanks to the original author of this repository [alstr](https://github.com/alstr), your work has saved me a significant amount of time here!
