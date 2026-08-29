---
icon: material/tag-outline
---

# Release

## Create a release

The recommended way to publish a release is through the GitHub based release
workflow.

### 1. Finalize the changelog

1. Rename `unreleased.md` to `changes_{X.Y.Z}.md`
2. Update the heading in `changes_{X.Y.Z}.md` to reflect the release version
   and add the release date:

    ```markdown
    # X.Y.Z - YYYY-MM-DD
    ```

3. Add the new file to the `nav` section in `zensical.toml`
4. Create a fresh `unreleased.md` for upcoming changes

### 2. Prepare the release

Bumps the project version and creates the corresponding commit:

```shell
invoke release.prepare X.Y.Z
```

### 3. Trigger the release workflow

Tags the release, pushes the tag and opens the pipeline in your browser:

```shell
invoke release.workflow X.Y.Z
```

!!! note

    Follow potential instructions printed by the tasks.

### What the pipeline does

Pushing the tag triggers the `ci-cd` workflow, which runs the following steps:

| Step             | Description                                                       |
|------------------|-------------------------------------------------------------------|
| Version check    | Verifies the pushed tag matches the version in `pyproject.toml`   |
| Checks & tests   | Runs formatting, linting, typing and the test suite               |
| Publish docs     | Publishes the docs as `X.Y.Z`, aliased as `latest`                |
| PyPi release     | Builds and uploads the distribution to PyPi                       |
| GitHub release   | Creates a GitHub release using the changelog as release notes     |

## Documentation

The documentation is built with [Zensical](https://zensical.org) and published
to the `gh-pages` branch. The published site always reflects the latest state:
it is rebuilt by the PR merge pipeline on `master` and again by the CI/CD
pipeline on a release tag.

### Working locally

```shell
invoke docs.serve   # preview the documentation (live reload)
invoke docs.build   # build the documentation into .html-documentation
invoke docs.clean   # remove the build artifacts
```

### Publishing manually

Publishing normally happens through the pipeline. To trigger it by hand, run
the `Publish Documentation` workflow from the GitHub Actions tab, or:

```shell
invoke release.docs
```
