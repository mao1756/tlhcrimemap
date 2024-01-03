# Git and GitHub Tutorial
This tutorial covers basic Git and GitHub operations that are useful for contributing to our project. Follow these steps to make your contributions smoothly.

**Important: Do NOT commit directly to the main branch to avoid conflicts. Please always follow the following procedure to push your changes to this repository**

## Cloning the project
To start working on the project, you first need to clone the repository to your local machine. Use the following command:

`git clone git@github.com:mao1756/tlhcrimemap.git`

You should set up SSH keys on your Git and GitHub account before running the command above. See [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) for details.

## Creating a new branch
Before making any changes, it's a good practice to create a new branch. This keeps your changes separate from the main codebase until they're ready to be merged. Use the following command:

`git checkout -b <branch-name>`

## Make Changes

Navigate to the project directory, and on the file `gittutorial`, write your name (or anything).

## Adding Changes to the Index

Once you've made your changes, you need to add them to the index. The index is a staging area where Git holds your changes before they are committed. It allows you to review and modify your changes before they become part of the commit history. To add your changes to the index, use:

`git add gittutorial`

You can also use `git add .` to add all of the files in the current directory.

## Committing Your Changes

`git commit -m "Your commit message`

Replace "Your commit message" with a brief description of your changes.

Good commit messages are crucial for maintaining a clear and efficient project history. A well-crafted commit message should be concise yet descriptive, allowing team members to understand the changes without needing to examine the code. Start with a short, imperative summary line (50 characters or less), like a command or suggestion: "Fix bug in payment gateway", followed by a blank line, and then a more detailed explanation if necessary. This explanation should provide context and rationale for the change, not just what was changed, but why. Avoid redundancy and keep it clear and to the point. Including references to related issue tracker IDs can be very helpful. Writing commit messages in this manner not only benefits others (and future you) who will read the commit history but also fosters a culture of transparency and collaboration within the team.

## Pushing Changes to GitHub
To share your changes with others and store them on the remote repository on GitHub, push your branch using:

`git push origin <branch-name>`

Again, avoid pushing to the main branch directly.

## Opening a Pull Request

Go to the GitHub page for our repository, and you'll see an option to create a 'Pull Request' for your branch. Open a pull request, describe your changes, and submit it for review.

## Approving the pull request

Ask the other member of your team to approve your pull request.

## Delete the branch from GitHub

Once the branch is merged, the option to delete the merged branch pops up. Follow the instructions to delete the branch.

## Delete the branch from your local repository

If your branch has been successfully merged into the main branch on GitHub (or any target branch in the upstream repository), you can follow these steps to update your local repository and clean up your branches:

### 1. Switch to Your Local Main Branch
First, switch to your local main branch.

`git checkout main`

### 2. Pull the Latest Changes

Fetch and merge the latest changes from the upstream repository. This will include the changes from the branch you just merged.

`git pull origin main`

### 3. Delete Your Local Feature Branch

`git branch -d <your-branch-name>`

Replace `<your-branch-name>` with the name of the branch you were working on. This command only deletes the branch locally. It won't affect the remote repository.
