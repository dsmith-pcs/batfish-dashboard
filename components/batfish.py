import pandas as pd
from pybatfish.client.session import Session
from pybatfish.datamodel import HeaderConstraints, Interface

# Global session for questions - will be set in __init__
_session = None

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)  # Changed from -1 to None for pandas 2.x compatibility

pd.options.display.float_format = '{:,}'.format


class Batfish():

    def __init__(self, batfish_host):
        self.batfish_host = batfish_host
        self.session = Session(host=batfish_host)
        # Set global session for backward compatibility
        global _session
        _session = self.session

    def delete_network(self, network):
        self.session.delete_network(network)

    def delete_snapshot(self, snapshot):
        self.session.delete_snapshot(snapshot)

    def set_snapshot(self, snapshot):
        self.session.set_snapshot(snapshot)

    def set_network(self, network):
        self.session.set_network(network)

    @property
    def get_existing_networks(self):
        return self.session.list_networks()

    @property
    def get_layer3_edges(self):
        result = self.session.q.layer3Edges().answer().frame()
        return result

    @property
    def get_interfaces(self):
        result = self.session.q.ipOwners().answer().frame()
        return result

    @property
    def get_ospf_edges(self):
        result = self.session.q.ospfEdges().answer().frame()
        return result

    @property
    def get_bgp_edges(self):
        result = self.session.q.bgpEdges().answer().frame()
        return result

    def get_existing_snapshots(self):
        try:
            snapshotlist = self.session.list_snapshots()
        except ValueError:
            snapshotlist = ["None"]
        return snapshotlist

    def init_snapshot(self, snapshot_name, overwrite=True):
        snapshot_dir = "assets/snapshot_holder/"
        self.session.init_snapshot(snapshot_dir, name=str(snapshot_name),
                                   overwrite=overwrite)

    def get_info(self, question_name):
        """
        Execute a Batfish question safely using getattr instead of eval.

        Args:
            question_name (str): Name of the Batfish question to execute

        Returns:
            pandas.DataFrame: Result of the question execution
        """
        # Validate the question name to prevent injection attacks
        if not question_name.isalnum():
            raise ValueError(f"Invalid question name: {question_name}")

        try:
            # Use getattr to safely get the question function from session
            question_func = getattr(self.session.q, question_name, None)
            if question_func is None:
                raise AttributeError(f"Question '{question_name}' not found")

            # Execute the question and return the result
            result = question_func().answer().frame()
            return result
        except Exception as e:
            print(f"Error executing question '{question_name}': {e}")
            # Return empty DataFrame on error
            return pd.DataFrame()



    def traceroute(self, src, dstIps, bidir,snapshot,
                   srcPorts=None,
                   dstPorts =None,
                   applications=None,
                   ipProtocols=None,
                   ):
        headers = HeaderConstraints(dstIps =dstIps,
                                    srcPorts=srcPorts,
                                    dstPorts =dstPorts,
                                    applications=applications,
                                    ipProtocols=ipProtocols)
        if bidir:
            result = self.session.q.bidirectionalTraceroute(startLocation=src,
                                                            headers=headers)\
                .answer(snapshot=snapshot)\
                .frame()
        else:

            result = self.session.q.traceroute(startLocation=src,
                                               headers=headers)\
                .answer(snapshot=snapshot)\
                .frame()
        return result

    def get_configuration(self, file_name, snapshot):
        return self.session.get_snapshot_input_object_text(file_name, snapshot=snapshot)

    def network_failure(self,
                        base_snapshot,
                        reference_snapshot,
                        deactivate_node,
                        deactivated_int,
                        overwrite=True):
        if not deactivated_int:
            self.session.fork_snapshot(base_snapshot,
                                       reference_snapshot,
                                       deactivate_nodes=deactivate_node,
                                       overwrite=overwrite)
        else:
            self.session.fork_snapshot(base_snapshot,
                                       reference_snapshot,
                                       deactivate_interfaces=[
                                           Interface(deactivate_node[0],
                                                     deactivated_int[0])
                                       ],
                                       overwrite=overwrite)



    def compare_acls(self, original_acl, refactored_acl, original_platform, refactored_platform):
        """
        Compare two ACLs using Batfish.

        Args:
            original_acl (str): Original ACL configuration text
            refactored_acl (str): Refactored ACL configuration text
            original_platform (str): Platform for original ACL
            refactored_platform (str): Platform for refactored ACL

        Returns:
            pandas.DataFrame: Comparison results
        """
        try:
            original_snapshot = self.session.init_snapshot_from_text(
                original_acl,
                platform=original_platform,
                snapshot_name="original",
                overwrite=True
            )
            refactored_snapshot = self.session.init_snapshot_from_text(
                refactored_acl,
                platform=refactored_platform,
                snapshot_name="refactored",
                overwrite=True
            )
            result = self.session.q.compareFilters().answer(
                snapshot=refactored_snapshot,
                reference_snapshot=original_snapshot
            ).frame()
            result.rename(
                columns={
                    'Line_Content': 'Refactored ACL Line',
                    'Reference_Line_Content': 'Original ACL Line'
                },
                inplace=True
            )
            return result
        except Exception as e:
            print(f"Error comparing ACLs: {e}")
            return pd.DataFrame()


    def get_question_description(self, question_name):
        """
        Get the description of a Batfish question safely.

        Args:
            question_name (str): Name of the Batfish question

        Returns:
            str: Description of the question
        """
        # Validate the question name to prevent injection attacks
        if not question_name.isalnum():
            raise ValueError(f"Invalid question name: {question_name}")

        try:
            # Use getattr to safely get the question function from session
            question_func = getattr(self.session.q, question_name, None)
            if question_func is None:
                raise AttributeError(f"Question '{question_name}' not found")

            # Get the description
            result = question_func().get_long_description()
            return result
        except Exception as e:
            print(f"Error getting description for question '{question_name}': {e}")
            return f"Description unavailable for question: {question_name}"

    @property
    def list_questions(self):
        # Return available questions by inspecting the session.q object
        try:
            # Get all available question methods from the session.q object
            question_methods = []
            if hasattr(self.session, 'q'):
                for attr_name in dir(self.session.q):
                    if not attr_name.startswith('_') and callable(getattr(self.session.q, attr_name, None)):
                        question_methods.append({'name': attr_name})
            return question_methods
        except Exception as e:
            print(f"Error listing questions: {e}")
            # Return a basic set of common questions as fallback
            return [
                {'name': 'layer3Edges'},
                {'name': 'ospfEdges'},
                {'name': 'bgpEdges'},
                {'name': 'ipOwners'},
                {'name': 'nodeProperties'},
                {'name': 'traceroute'},
                {'name': 'reachability'},
                {'name': 'compareFilters'},
            ]