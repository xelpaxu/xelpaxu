# Install the profile dashboard

1. Clone or open your existing public profile repository, `xelpaxu/xelpaxu`. Keep its Git history so you can restore the current README if you change your mind.
2. Copy `README.md`, `assets/`, `scripts/`, and `.github/workflows/refresh-profile.yml` into the repository root. The archive includes the hidden `.github` directory. Merge the folders with any existing files.
3. Commit the files and push them to your default branch.
4. If the repository already has a working `PROFILE_STATS_TOKEN` secret, keep it and skip to step 5. Otherwise, create a GitHub personal access token (classic) with the `public_repo` scope for the GraphQL queries. Skip the `repo` and `read:user` scopes to keep this dashboard focused on public information. Store the token in the profile repository under **Settings → Secrets and variables → Actions → New repository secret** as `PROFILE_STATS_TOKEN`. Keep the token out of the README and the repository files.
5. Open your repository's **Actions** tab, select **Refresh profile dashboard**, and choose **Run workflow**. The first successful run replaces the initial activity cards and adds collapsible charts by year. Scheduled updates run nightly, around 1:23 a.m. Philippine time, subject to GitHub's scheduling delays.

After a successful run, the README contains updated contribution totals and image URLs with content versions. The dark SVGs live under `assets/dark/`.

The workflow uses the repository's automatic token to commit generated files. If a rule blocks its push, the workflow log will identify the affected branch rule.

To edit the terminal bio, project cards, or colors, change `render_static()` in `scripts/render.py`, then run the workflow again. Edit project destinations directly in `README.md`. The refresh script updates the activity block between the two HTML comments and leaves the other README text intact.

[GitHub profile README documentation](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)

[GitHub GraphQL authentication and token scopes](https://docs.github.com/en/graphql/guides/forming-calls-with-graphql)
