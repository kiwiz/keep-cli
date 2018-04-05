import keyring
import gkeepapi
import curses
import yaml

fh = open('config.yml', 'r')
config = yaml.load(fh, Loader=yaml.Loader)
fh.close()

password = keyring.get_password('google-keep', config['username'])

keep = gkeepapi.Keep()
keep.login(config['username'], password)

def main(stdscr):
    todo = keep.findLabel('todo')

    notes = keep.find(archived=False, trashed=False, labels=[todo])

    for note in notes:
        if note.id in config['ignore']:
            continue
        print('-', note.title if note.title else note.text, note.id)

curses.wrapper(main)
