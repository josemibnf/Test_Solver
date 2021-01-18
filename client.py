import grpc
import instances_pb2, instances_pb2_grpc
import requests

NODE_URI = "192.168.1.64:8000"
RANDOM_CNF = ""
SOLVER = ""


def is_good(cnf, interpretation):
    def good_clause(clause, interpretation):
        for var in clause.literal:
            for i in interpretation.variable:
                if var == i:
                    return True
        return False

    for clause in cnf.clause:
        if not good_clause(clause, interpretation):
            return False
    return True


if __name__ == "__main__":
    random_uri = requests.get(
        'http://' + NODE_URI,
        json={
            "service": RANDOM_CNF
        })
    random_uri = random_uri.json()['uri']
    print('RANDOM URI -> ', random_uri)

    try:
        cnf = instances_pb2_grpc.ServiceStub(
                grpc.insecure_channel(random_uri)
            ).RandomCnf(instances_pb2.WhoAreYourParams())
    except (grpc.RpcError, TimeoutError) as e:
        print('Error '+ str(e))
        exit()

    print('CNF --> ', cnf)

    solver_uri = requests.get(
        'http://' + NODE_URI,
        json={
            "service": RANDOM_CNF
        })
    solver_uri = solver_uri.json()['uri']
    print('SOLVER URI --> ', solver_uri)

    try:
        interpretation = instances_pb2_grpc.SolverStub(
            grpc.insecure_channel(target=solver_uri)
        ).Solve(cnf)
    except (grpc.RpcError, TimeoutError) as e:
        print('Error '+ str(e))
        exit()

    print('INTERPRATAION --> ', interpretation)

    print('IS GOOD INTERPRETATION --> ', is_good(cnf=cnf, interpretation=interpretation))
