from lk_elections.core import ElectionFPTP

class UnusualStats:

    def analyze_election(self, election):
        print(f'## {election.date_str}')
        for result in election.results:
            summary = result.summary
            if summary.electors == 0:
                continue

            p_turnout = summary.p_turnout
            if p_turnout > 1:
                print(f'* {result.electorate_name} {p_turnout:.0%}')

    def analyze(self):
        elections =  ElectionFPTP.list_all()    
        for election in elections:
            self.analyze_election(election)


def main():
    UnusualStats().analyze()    


if __name__ == "__main__":
    main()