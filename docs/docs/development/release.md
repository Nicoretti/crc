# Release

## Create a release using the GitHub release workflow

1. Rename `unreleased.md` to `changes_{X.Y.Z}.md`
2. Update heading in `changes_{X.Y.Z}.md` to reflect the release version
3. Add the current date behind the release number
   ```markdown
   # X.Y.Z - YYYY-MM-DD
   ```
4. Prepare the release
   ```console
   uv run camas release_prepare --VERSION X.Y.Z
   ```
5. Run the CI/CD pipeline to publish the release:
   ```console
   uv run camas release_workflow --VERSION X.Y.Z
   ```
