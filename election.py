from dataclasses import dataclass, field
import re


# The Candidate class features data of given candidate, including name, last name, number of votes, constituency
# and whether the candidate still participates in the election.
@dataclass
class Candidate:
    name: str
    last_name: str
    votes_count: int
    constituency: str
    participates_in_election: bool = True


# The Elector class contains data about en elector, including constituency and a list of candidates for whom
# the voter can cast a vote.
@dataclass
class Elector:
    constituency: str
    candidates: list[Candidate] = field(default_factory=lambda: [])


# The TextFileRead class is responsible for working with text files and parse them to match expected data type.
class TextFileReader:

    # Method gets candidates from file candidates.txt
    @staticmethod
    def get_candidates(filename: str, pattern: str) -> list[Candidate]:
        candidates = []

        with open(filename, 'r') as f:
            for line in f.readlines():
                if not re.match(pattern, line):
                    raise ValueError('Candidate form in text file is not correct')

                candidate_data = line.strip().split(', ')
                candidates.append(Candidate(candidate_data[0], candidate_data[1], int(candidate_data[2]), candidate_data[3]))

        return candidates

    # Method get electors from file electors.txt
    @staticmethod
    def get_electors(filename: str, pattern: str) -> list[Elector]:
        electors = []

        with open(filename, 'r') as f:
            for line in f.readlines():
                if not re.match(pattern, line):
                    raise ValueError('Elector form in text file is not correct')

                elector_data = line.strip().replace(',', '')
                electors.append(Elector(elector_data))

        return electors


def main() -> None:
    electors = TextFileReader.get_electors('electors.txt', r'^O\d+$')
    print(f'Electors: {electors}')

    candidates = TextFileReader.get_candidates('candidates.txt', r'^([A-Z][a-z]+, ){2}0{1}, O\d+$')
    print(f'Candidates: {candidates}')

if __name__ == '__main__':
    main()