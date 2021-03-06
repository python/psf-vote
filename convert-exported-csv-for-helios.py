"""Script to convert voter data for Helios Voting.

This script expects a CSV generated from an Excel/Google Docs export based
off of CivicCRM data.

The format of the CSV is vaguely: firstname,lastname,email

The desired output for Helios is: uniqueid,email,name
"""
import argparse
import csv
import uuid


def generate_unique_id():
    """Create a UUID for our voter."""
    return uuid.uuid4().hex


def create_parser():
    """Create our argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--from', dest='source',
        type=argparse.FileType('r'),
        help='CSV file based on CivicCRM data',
    )
    parser.add_argument(
        '--to', dest='destination',
        type=argparse.FileType('w'),
        help='CSV file based on CivicCRM data',
    )
    return parser


def convert(from_source, to_destination):
    """Handle conversion of the data."""
    civicrm_reader = csv.reader(from_source, delimiter=',')
    helios_writer = csv.writer(to_destination, delimiter=',')
    for row in civicrm_reader:
        row = [col.strip() for col in row]
        email = row.pop()
        if ',' in row[-1]:
            row[-1] = row[-1].split(',')[0]
        if '@' in row[-1]:
            row[-1] = ''
        userid = generate_unique_id()
        # NOTE(sigmavirus24): We strip here because if the name is ' ' we want
        # to be able to easily check for an empty name. In that case, we want
        # to give the voter a name to ensure they receive a ballot.
        # See also:
        # https://github.com/benadida/helios-server/issues/197#issuecomment-396616993
        name = ' '.join(row).strip()
        if name == '':
            name = f'PSF Voter {userid}'
        helios_writer.writerow([userid, email, name])


def main():
    """Run the conversion."""
    parser = create_parser()
    args = parser.parse_args()
    convert(args.source, args.destination)


if __name__ == '__main__':
    main()
