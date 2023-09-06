from dataclasses import dataclass, field
import re
from collections import defaultdict
from typing import Self


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


# The Election class includes summary of constituency and matching candidates and a list of all electors.
# In this class a vote is held and the winner is selected.
@dataclass
class Election:
    constituency_and_candidates: dict[str, list[Candidate]]
    electors: list[Elector]

    # The method adds candidates to an elector based on constituency.
    def add_candidates_to_elector(self) -> None:
        for e in self.electors:
            for c in self.constituency_and_candidates.values():
                e.candidates.extend([i for i in c if i.constituency == e.constituency])

    # The method holds a vote.
    def vote(self) -> None:
        for elector in self.electors:
            print(f'Constituency: {elector.constituency}')
            for index, candidate in enumerate(elector.candidates, start=1):
                if candidate.participates_in_election:
                    print(f'{index}. {candidate.name} {candidate.last_name}')

            vote = int(input('Your vote (candidate number):\n'))
            if 0 < vote <= len(elector.candidates):
                elector.candidates[vote - 1].votes_count += 1

    # The method selects a list of leader or leaders, depending on the number of votes cast.
    def get_the_leader(self) -> list[Candidate]:
        candidates_and_votes = defaultdict(list)
        for candidates in self.constituency_and_candidates.values():
            for c in candidates:
                if c.participates_in_election:
                    candidates_and_votes[c.votes_count].append(c)

        return max(candidates_and_votes.items(), key=lambda x: x[0])[1]

    # The method holds elections.
    def conduct_elections(self) -> list[Candidate]:
        self.add_candidates_to_elector()

        self.vote()
        leaders = self.get_the_leader()

        while len(leaders) > 1:
            print('No leader emerged.')

            for constituency, candidates in self.constituency_and_candidates.items():

                for candidate in candidates:
                    if candidate not in leaders:
                        candidate.participates_in_election = False

            self.vote()
            leaders = self.get_the_leader()

        return leaders

    # The method gets data about the candidates and electors from text files via class TextFileReader.
    @classmethod
    def get_data(cls) -> Self:
        candidates = TextFileReader.get_candidates('candidates.txt', r'^([A-Z][a-z]+, ){2}0{1}, O\d+$')
        pairs = defaultdict(list)
        for c in candidates:
            pairs[c.constituency].append(c)

        electors = TextFileReader.get_electors('electors.txt', r'^O\d+$')

        return cls(dict(pairs), electors)


def main() -> None:
    data = Election.get_data()

    print(f'Winner: {data.conduct_elections()}')

if __name__ == '__main__':
    main()