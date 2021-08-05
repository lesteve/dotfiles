import re
import pathlib
import warnings
import difflib
import argparse
import argparse


def get_info(filename):
    for line in open(filename):
        channel_match = re.match(r'Channel (\w+)', line)
        if channel_match:
            channel = channel_match.group(1)

        imap_folder_match = re.match(
            r'Opening slave box (\S+)\.{3}',
            line)
        if imap_folder_match:
            imap_folder = imap_folder_match.group(1)

        uid_validity_match = re.match(
            r'Error: UIDVALIDITY of master changed \(got (\d+), expected (\d+)\)',
            line)
        if uid_validity_match:
            uid_from_server = uid_validity_match.group(1)
            uid_from_log = uid_validity_match.group(2)
            yield channel, imap_folder, uid_from_server, uid_from_log


def get_mbsync_path(channel, imap_folder):
    base_maildir_path = pathlib.Path('~/.mail').expanduser()
    maildir_folder = base_maildir_path / channel / imap_folder
    if not maildir_folder.exists():
        raise RuntimeError(f'Did not find maildir folder: {maildir_folder}')

    mbsyncstate_path = maildir_folder.joinpath('.mbsyncstate')
    if not mbsyncstate_path.exists():
        raise FileNotFoundError(f'{mbsyncstate_path} not found')

    return mbsyncstate_path


def fix_uid_validity(path, uid_from_server, uid_from_log, dry_run=False):
    content = path.read_text()
    uid_match = re.search(r'^MasterUidValidity (\d+)$', content,
                          flags=re.MULTILINE)
    if uid_match is None:
        raise RuntimeError(f'Could not find MasterUidValidity in file {path}')
    uid_from_file = uid_match.group(1)
    if uid_from_file != uid_from_log:
        # only a warning. Use case: you want to rerun from an old log
        warnings.warn('Mismatch between uid in log and file.'
                      f'Ignoring {path}')
        return
    new_content = content.replace(f'MasterUidValidity {uid_from_file}',
                                  f'MasterUidValidity {uid_from_server}')

    if dry_run:
        print('-' * 80)
        print('path:', path)
        print('\n'.join(difflib.unified_diff(content.splitlines(), new_content.splitlines())))

    else:
        path.write_text(new_content)


def main(log_filename='/tmp/mbsync.log', dry_run=False):
    info = list(get_info(log_filename))
    print(f'Found {len(info)} UIDVALIDITY problem in {log_filename}')
    for channel, imap_folder, uid_from_server, uid_from_log in info:
        mbsync_path = get_mbsync_path(channel, imap_folder)
        fix_uid_validity(mbsync_path, uid_from_server, uid_from_log,
                         dry_run=dry_run)


parser = argparse.ArgumentParser(
    description='Fix UIDVALIDITY in .mbsyncstate using mbsync log.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('log_filename', default='/tmp/mbsync.log', nargs='?',
                    help='mbsync log file')
parser.add_argument('--dry-run', action='store_const', const=True,
                    default=False,
                    help='Perform a dry run')

if __name__ == '__main__':
    args = parser.parse_args()
    main(log_filename=args.log_filename,
         dry_run=args.dry_run)
