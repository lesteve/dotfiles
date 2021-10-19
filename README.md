To install it on a new computer (adapted from
https://www.atlassian.com/git/tutorials/dotfiles):

```sh
GIT_REPO_DIR=$HOME/.dotfiles.git
BACKUP_DIR=$HOME/.config-backup

git clone --bare https://github.com/lesteve/dotfiles $GIT_REPO_DIR
alias dotfiles="git --git-dir=$GIT_REPO_DIR --work-tree=$HOME"

mkdir -p $BACKUP_DIR
dotfiles checkout
if [ $? = 0 ]; then
  echo "Checked out dotfiles.";
  else
    echo "Backing up pre-existing dot files.";
    dotfiles checkout 2>&1 | egrep "\s+\." | awk {'print $1'} | xargs -I{} mv {} $BACKUP_DIR/{}
fi;
dotfiles checkout
dotfiles submodule update --init
dotfiles config status.showUntrackedFiles no
```
