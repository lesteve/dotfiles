To install it on a new computer:

```sh
DOTFILES_DIR=$HOME/dev/dotfiles

git clone --recursive https://github.com/lesteve/dotfiles $DOTFILES_DIR
stow --target ~ --dir $DOTFILES_DIR -S .
# TODO there will be some errors if files already exists
```

