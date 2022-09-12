import csv
import sys


def main():

    # TODO: Check for command-line usage
    # Handle command line arguments
    if len(sys.argv) != 3:
        print("Usage: python dna.py data sequence")
        exit(1)

    db_path = "./" + sys.argv[1]
    seq_path = "./" + sys.argv[2]

    # TODO: Read database file into a variable
    db = {}
    with open(db_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        db = list(reader)

    # TODO: Read DNA sequence file into a variable
    sequence = []
    with open(seq_path, "r") as inputfileseq:
        sequence = inputfileseq.read()

    # TODO: Find longest match of each STR in DNA sequence
    sequences = {"AGATC": 0, "AATG": 0, "TATC": 0}
    for seq in sequences:
        ret = longest_match(sequence, seq)
        sequences[seq] += ret

    # TODO: Check database for matching profiles
    identity = 'No Match'

    AGATC = str(sequences['AGATC'])
    AATG = str(sequences['AATG'])
    TATC = str(sequences['TATC'])

    for person in db:
        if person['AGATC'] == AGATC and person['AATG'] == AATG and person['TATC'] == TATC:
            identity = person['name']

    print(identity)
    # people = [

    # {'name': "Tom", 'age': 10},
    # {'name': "Mark", 'age': 5},
    # {'name': "Pam", 'age': 7}
    # ]

    # for person in people:
    #    if person['name'] == "Mark":
    #        print(person)

    # print(filter(lambda person: person['name'] == 'Pam', people))


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
