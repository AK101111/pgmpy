import unittest
from pgmpy.readwrite import PomdpXReader
import os


class TestPomdpXReaderString(unittest.TestCase):
    def setUp(self):
        self.reader = PomdpXReader(string="""
   <pomdpx version="1.0" id="rockSample"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="pomdpx.xsd">
         <Description>RockSample problem for map size 1 x 3.
           Rock is at 0, Rover’s initial position is at 1.
           Exit is at 2.
         </Description>
         <Discount>0.95</Discount>
         <Variable>
              <StateVar vnamePrev="rover_0" vnameCurr="rover_1"
                fullyObs="true">
                  <NumValues>3</NumValues>
              </StateVar>
              <StateVar vnamePrev="rock_0" vnameCurr="rock_1">
                  <ValueEnum>good bad</ValueEnum>
              </StateVar>
              <ObsVar vname="obs_sensor">
                  <ValueEnum>ogood obad</ValueEnum>
              </ObsVar>
              <ActionVar vname="action_rover">
                  <ValueEnum>amw ame ac as</ValueEnum>
              </ActionVar>
              <RewardVar vname="reward_rover" />
         </Variable>
         <InitialStateBelief>
              <CondProb>
                  <Var>rover_0</Var>
                  <Parent>null</Parent>
                  <Parameter type="TBL">
                        <Entry>
                            <Instance> - </Instance>
                            <ProbTable>0.0 1.0 0.0</ProbTable>
                        </Entry>
              </Parameter>
         </CondProb>
         <CondProb>
              <Var>rock_0</Var>
              <Parent>null</Parent>
              <Parameter type="TBL">
                  <Entry>
                      <Instance>-</Instance>
                      <ProbTable>uniform</ProbTable>
                  </Entry>
              </Parameter>
         </CondProb>
      </InitialStateBelief>
      <StateTransitionFunction>
          <CondProb>
              <Var>rover_1</Var>
              <Parent>action_rover rover_0</Parent>
              <Parameter type="TBL">
                  <Entry>
                      <Instance>amw s0 s2</Instance>
                      <ProbTable>1.0</ProbTable>
                  </Entry>
                  <Entry>
                      <Instance>amw s1 s0</Instance>
                      <ProbTable>1.0</ProbTable>
                  </Entry>
                  <Entry>
                      <Instance>ame s0 s1</Instance>
                      <ProbTable>1.0</ProbTable>
                  </Entry>
                  <Entry>
                      <Instance>ame s1 s2</Instance>
                      <ProbTable>1.0</ProbTable>
                  </Entry>
                  <Entry>
                      <Instance>ac s0 s0</Instance>
                      <ProbTable>1.0</ProbTable>
                  </Entry>
                  <Entry>
                      <Instance>ac s1 s1</Instance>
                      <ProbTable>1.0</ProbTable>
                  </Entry>
                  <Entry>
                      <Instance>as s0 s0</Instance>
                      <ProbTable>1.0</ProbTable>
                  </Entry>
                  <Entry>
                      <Instance>as s1 s2</Instance>
                      <ProbTable>1.0</ProbTable>
                  </Entry>
                  <Entry>
                      <Instance>* s2 s2</Instance>
                      <ProbTable>1.0</ProbTable>
                  </Entry>
           </Parameter>
       </CondProb>
       <CondProb>
           <Var>rock_1</Var>
           <Parent>action_rover rover_0 rock_0</Parent>
           <Parameter>
               <Entry>
                   <Instance>amw * - - </Instance>
                   <ProbTable>1.0 0.0 0.0 1.0</ProbTable>
               </Entry>
               <Entry>
                   <Instance>ame * - - </Instance>
                   <ProbTable>identity</ProbTable>
               </Entry>
               <Entry>
                   <Instance>ac * - - </Instance>
                   <ProbTable>identity</ProbTable>
               </Entry>
               <Entry>
                   <Instance>as * - - </Instance>
                   <ProbTable>identity</ProbTable>
               </Entry>
               <Entry>
                   <Instance>as s0 * - </Instance>
                   <ProbTable>0.0 1.0</ProbTable>
               </Entry>
           </Parameter>
       </CondProb>
   </StateTransitionFunction>
   <ObsFunction>
       <CondProb>
           <Var>obs_sensor</Var>
           <Parent>action_rover rover_1 rock_1</Parent>
           <Parameter type="TBL">
               <Entry>
                   <Instance>amw * * - </Instance>
                   <ProbTable>1.0 0.0</ProbTable>
               </Entry>
               <Entry>
                   <Instance>ame * * - </Instance>
                   <ProbTable>1.0 0.0</ProbTable>
               </Entry>
               <Entry>
                   <Instance>as * * - </Instance>
                   <ProbTable>1.0 0.0</ProbTable>
               </Entry>
               <Entry>
                   <Instance>ac s0 - - </Instance>
                   <ProbTable>1.0 0.0 0.0 1.0</ProbTable>
               </Entry>
               <Entry>
                   <Instance>ac s1 - - </Instance>
                   <ProbTable>0.8 0.2 0.2 0.8</ProbTable>
               </Entry>
                <Entry>
                     <Instance>ac s2 * - </Instance>
                     <ProbTable>1.0 0.0</ProbTable>
                </Entry>
            </Parameter>
        </CondProb>
    </ObsFunction>
    <RewardFunction>
        <Func>
            <Var>reward_rover</Var>
            <Parent>action_rover rover_0 rock_0</Parent>
            <Parameter type="TBL">
                <Entry>
                     <Instance>ame s1 *</Instance>
                     <ValueTable>10</ValueTable>
                </Entry>
                <Entry>
                     <Instance>amw s0 *</Instance>
                     <ValueTable>-100</ValueTable>
                </Entry>
                <Entry>
                     <Instance>as s1 *</Instance>
                     <ValueTable>-100</ValueTable>
                </Entry>
                <Entry>
                     <Instance>as s0 good</Instance>
                     <ValueTable>10</ValueTable>
                </Entry>
                <Entry>
                     <Instance>as s0 bad</Instance>
                     <ValueTable>-10</ValueTable>
                </Entry>
            </Parameter>
        </Func>
    </RewardFunction>
 </pomdpx>
 """)

    def test_get_variables(self):
        var_expected = {'StateVar': [
                        {'vnamePrev': 'rover_0',
                         'vnameCurr': 'rover_1',
                         'ValueEnum': ['s0', 's1', 's2'],
                         'fullyObs': True},
                        {'vnamePrev': 'rock_0',
                         'vnameCurr': 'rock_1',
                         'fullyObs': False,
                         'ValueEnum': ['good', 'bad']}],
                        'ObsVar': [{'vname': 'obs_sensor',
                                    'ValueEnum': ['ogood', 'obad']}],
                        'RewardVar': [{'vname': 'reward_rover'}],
                        'ActionVar': [{'vname': 'action_rover',
                                       'ValueEnum': ['amw', 'ame',
                                                     'ac', 'as']}]
                        }
        self.maxDiff = None
        self.assertEqual(self.reader.get_variables(), var_expected)

    def test_get_initial_belief_system(self):
        belief_expected = [{'Var': 'rover_0',
                            'Parent': ['null'],
                            'Type': 'TBL',
                            'Parameter': [{'Instance': ['-'],
                                           'ProbTable': ['0.0', '1.0', '0.0']}]
                            },
                           {'Var': 'rock_0',
                            'Parent': ['null'],
                            'Type': 'TBL',
                            'Parameter': [{'Instance': ['-'],
                                           'ProbTable': ['uniform']}]
                            }]
        self.maxDiff = None
        self.assertEqual(self.reader.get_initial_beliefs(), belief_expected)

    def test_get_state_transition_function(self):
        state_transition_function_expected = \
            [{'Var': 'rover_1',
              'Parent': ['action_rover', 'rover_0'],
              'Type': 'TBL',
              'Parameter': [{'Instance': ['amw', 's0', 's2'],
                             'ProbTable': ['1.0']},
                            {'Instance': ['amw', 's1', 's0'],
                             'ProbTable': ['1.0']},
                            {'Instance': ['ame', 's0', 's1'],
                             'ProbTable': ['1.0']},
                            {'Instance': ['ame', 's1', 's2'],
                             'ProbTable': ['1.0']},
                            {'Instance': ['ac', 's0', 's0'],
                             'ProbTable': ['1.0']},
                            {'Instance': ['ac', 's1', 's1'],
                             'ProbTable': ['1.0']},
                            {'Instance': ['as', 's0', 's0'],
                             'ProbTable': ['1.0']},
                            {'Instance': ['as', 's1', 's2'],
                             'ProbTable': ['1.0']},
                            {'Instance': ['*', 's2', 's2'],
                             'ProbTable': ['1.0']}]},
             {'Var': 'rock_1',
              'Parent': ['action_rover', 'rover_0', 'rock_0'],
              'Type': 'TBL',
              'Parameter': [{'Instance': ['amw', '*', '-', '-'],
                             'ProbTable': ['1.0', '0.0', '0.0', '1.0']},
                            {'Instance': ['ame', '*', '-', '-'],
                             'ProbTable': ['identity']},
                            {'Instance': ['ac', '*', '-', '-'],
                             'ProbTable': ['identity']},
                            {'Instance': ['as', '*', '-', '-'],
                             'ProbTable': ['identity']},
                            {'Instance': ['as', 's0', '*', '-'],
                             'ProbTable': ['0.0', '1.0']},
                            ]}]
        self.maxDiff = None
        self.assertEqual(self.reader.get_state_transition_function(),
                         state_transition_function_expected)

    def test_obs_function(self):
        obs_function_expected = \
            [{'Var': 'obs_sensor',
              'Parent': ['action_rover', 'rover_1', 'rock_1'],
              'Type': 'TBL',
              'Parameter': [{'Instance': ['amw', '*', '*', '-'],
                             'ProbTable': ['1.0', '0.0']},
                            {'Instance': ['ame', '*', '*', '-'],
                             'ProbTable': ['1.0', '0.0']},
                            {'Instance': ['as', '*', '*', '-'],
                             'ProbTable': ['1.0', '0.0']},
                            {'Instance': ['ac', 's0', '-', '-'],
                             'ProbTable': ['1.0', '0.0', '0.0', '1.0']},
                            {'Instance': ['ac', 's1', '-', '-'],
                             'ProbTable': ['0.8', '0.2', '0.2', '0.8']},
                            {'Instance': ['ac', 's2', '*', '-'],
                             'ProbTable': ['1.0', '0.0']}]}]
        self.maxDiff = None
        self.assertEqual(self.reader.get_obs_function(), obs_function_expected)

    def test_reward_function(self):
        reward_function_expected = \
            [{'Var': 'reward_rover',
              'Parent': ['action_rover', 'rover_0', 'rock_0'],
              'Type': 'TBL',
              'Parameter': [{'Instance': ['ame', 's1', '*'],
                             'ValueTable': ['10']},
                            {'Instance': ['amw', 's0', '*'],
                             'ValueTable': ['-100']},
                            {'Instance': ['as', 's1', '*'],
                             'ValueTable': ['-100']},
                            {'Instance': ['as', 's0', 'good'],
                             'ValueTable': ['10']},
                            {'Instance': ['as', 's0', 'bad'],
                             'ValueTable': ['-10']}]}]
        self.maxDiff = None
        self.assertEqual(self.reader.get_reward_function(),
                         reward_function_expected)

    def test_get_parameter_dd(self):
        self.reader = PomdpXReader(string="""
        <pomdpx version="1.0" id="rockSample"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="pomdpx.xsd">
         <Description>RockSample problem for map size 1 x 3.
           Rock is at 0, Rover’s initial position is at 1.
           Exit is at 2.
         </Description>
         <Discount>0.95</Discount>
        <InitialStateBelief>
        <CondProb>
         <Var>rover_0</Var>
  <Parent>null</Parent>
   <Parameter type = "DD">
      <DAG>
         <Node var = "rover_0">
             <Edge val="s0"><Terminal>0.0</Terminal></Edge>
              <Edge val="s1">
                 <Node var = "rock_0">
                     <Edge val = "good">
                       <Terminal>0.5</Terminal>
                  </Edge>
                   <Edge val = "bad">
                      <Terminal>0.5</Terminal>
                   </Edge>
                </Node>
           </Edge>
           <Edge val="s2"><Terminal>0.0</Terminal></Edge>
         </Node>
      </DAG>
  </Parameter>
  </CondProb>
  </InitialStateBelief>
  </pomdpx>
 """)
        expected_dd_parameter = [{
            'Var': 'rover_0',
            'Parent': ['null'],
            'Type': 'DD',
            'Parameter': {'rover_0': {'s0': '0.0',
                                      's1': {'rock_0': {'good': '0.5',
                                                        'bad': '0.5'}},
                                      's2': '0.0'}}}]
        self.maxDiff = None
        self.assertEqual(expected_dd_parameter,
                         self.reader.get_initial_beliefs())

    def test_initial_belief_dd(self):
        self.reader = PomdpXReader(string="""
    <pomdpx version="1.0" id="rockSample"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="pomdpx.xsd">
         <Description>RockSample problem for map size 1 x 3.
           Rock is at 0, Rover’s initial position is at 1.
           Exit is at 2.
         </Description>
         <Discount>0.95</Discount>
        <InitialStateBelief>
        <CondProb>
            <Var>rover_0</Var>
            <Parent>null</Parent>
            <Parameter type="DD">
                <DAG>
                    <Node var="rover_0">
                        <Edge val="s0">
                            <Terminal>0.0</Terminal>
                        </Edge>
                        <Edge val="s1">
                            <SubDAG type="uniform" var="rock_0"/>
                        </Edge>
                        <Edge val="s2">
                            <Terminal>0.0</Terminal>
                        </Edge>
                    </Node>
                </DAG>
            </Parameter>
        </CondProb>
    </InitialStateBelief>
    </pomdpx>
    """)
        expected_belief_dd = [{
            'Var': 'rover_0',
            'Parent': ['null'],
            'Type': 'DD',
            'Parameter': {'rover_0': {'s0': '0.0',
                                      's1': {'type': 'uniform',
                                             'var': 'rock_0'},
                                      's2': '0.0'}}}]
        self.maxDiff = None
        self.assertEqual(self.reader.get_initial_beliefs(),
                         expected_belief_dd)

    def test_reward_function(self):
        self.reader = PomdpXReader(string="""
        <pomdpx version="1.0" id="rockSample"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="pomdpx.xsd">
         <Description>RockSample problem for map size 1 x 3.
           Rock is at 0, Rover’s initial position is at 1.
           Exit is at 2.
         </Description>
         <Discount>0.95</Discount>
        <RewardFunction>
        <Func>
            <Var>reward_rover</Var>
            <Parent>action_rover rover_0 rock_0</Parent>
            <Parameter type="DD">
                <DAG>
                    <Node var="action_rover">
                        <Edge val="amw">
                            <Node var="rover_0">
                                <Edge val="s0">
                                    <Terminal>-100.0</Terminal>
                                </Edge>
                                <Edge val="s1">
                                    <Terminal>0.0</Terminal>
                                </Edge>
                                <Edge val="s2">
                                    <Terminal>0.0</Terminal>
                                </Edge>
                            </Node>
                        </Edge>
                        <Edge val="ame">
                            <Node var="rover_0">
                                <Edge val="s0">
                                    <Terminal>0.0</Terminal>
                                </Edge>
                                <Edge val="s1">
                                    <Terminal>10.0</Terminal>
                                </Edge>
                                <Edge val="s2">
                                    <Terminal>0.0</Terminal>
                                </Edge>
                            </Node>
                        </Edge>
                        <Edge val="ac">
                            <Terminal>0.0</Terminal>
                        </Edge>
                        <Edge val="as">
                            <Node var="rover_0">
                                <Edge val="s0">
                                    <Node var="rock_0">
                                        <Edge val="good">
                                            <Terminal>10</Terminal>
                                        </Edge>
                                        <Edge val="bad">
                                            <Terminal>-10</Terminal>
                                        </Edge>
                                    </Node>
                                </Edge>
                                <Edge val="s1">
                                    <Terminal>-100</Terminal>
                                </Edge>
                                <Edge val="s2">
                                    <Terminal>-100</Terminal>
                                </Edge>
                            </Node>
                        </Edge>
                    </Node>
                </DAG>
            </Parameter>
        </Func>
    </RewardFunction>
    </pomdpx>
        """)
        expected_reward_function_dd =\
            [{'Var': 'reward_rover',
              'Parent': ['action_rover', 'rover_0', 'rock_0'],
              'Type': 'DD',
              'Parameter': {'action_rover': {'amw': {'rover_0': {'s0': '-100.0',
                                                                 's1': '0.0',
                                                                 's2': '0.0'}},
                                             'ame': {'rover_0': {'s0': '0.0',
                                                                 's1': '10.0',
                                                                 's2': '0.0'}},
                                             'ac': '0.0',
                                             'as': {'rover_0': {'s0': {'rock_0': {'good': '10',
                                                                                  'bad': '-10'}},
                                                                's1': '-100',
                                                                's2': '-100'}}}}}]
        self.maxDiff = None
        self.assertEqual(self.reader.get_reward_function(),
                         expected_reward_function_dd)

    def test_state_transition_function(self):
        self.reader = PomdpXReader(string="""
         <pomdpx version="1.0" id="rockSample"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="pomdpx.xsd">
         <Description>RockSample problem for map size 1 x 3.
           Rock is at 0, Rover’s initial position is at 1.
           Exit is at 2.
         </Description>
         <Discount>0.95</Discount>
        <StateTransitionFunction>
        <CondProb>
            <Var>rover_1</Var>
            <Parent>action_rover rover_0</Parent>
            <Parameter type="DD">
                <DAG>
                    <Node var="action_rover">
                        <Edge val="amw">
                            <Node var="rover_0">
                                <Edge val="s0">
                                    <SubDAG type="deterministic" var="rover_1" val="s2"/>
                                </Edge>
                                <Edge val="s1">
                                    <SubDAG type="deterministic" var="rover_1" val="s0"/>
                                </Edge>
                                <Edge val="s2">
                                    <SubDAG type="deterministic" var="rover_1" val="s2"/>
                                </Edge>
                            </Node>
                        </Edge>
                        <Edge val="ame">
                            <Node var="rover_0">
                                <Edge val="s0">
                                    <SubDAG type="deterministic" var="rover_1" val="s1"/>
                                </Edge>
                                <Edge val="s1">
                                    <SubDAG type="deterministic" var="rover_1" val="s2"/>
                                </Edge>
                                <Edge val="s2">
                                    <SubDAG type="deterministic" var="rover_1" val="s2"/>
                                </Edge>
                            </Node>
                        </Edge>
                        <Edge val="ac">
                            <SubDAG type="persistent" var="rover_1"/>
                        </Edge>
                        <Edge val="as">
                            <Node var="rover_0">
                                <Edge val="s0">
                                    <SubDAG type="deterministic" var="rover_1" val="s0"/>
                                </Edge>
                                <Edge val="s1">
                                    <SubDAG type="deterministic" var="rover_1" val="s2"/>
                                </Edge>
                                <Edge val="s2">
                                    <SubDAG type="deterministic" var="rover_1" val="s2"/>
                                </Edge>
                            </Node>
                        </Edge>
                    </Node>
                </DAG>
            </Parameter>
        </CondProb>
        <CondProb>
            <Var>rock_1</Var>
            <Parent>action_rover rover_0 rock_0</Parent>
            <Parameter type="DD">
                <DAG>
                    <Node var="action_rover">
                        <Edge val="amw">
                            <SubDAG type="persistent" var="rock_1"/>
                        </Edge>
                        <Edge val="ame">
                            <SubDAG type="persistent" var="rock_1"/>
                        </Edge>
                        <Edge val="ac">
                            <SubDAG type="persistent" var="rock_1"/>
                        </Edge>
                        <Edge val="as">
                            <Node var="rover_0">
                                <Edge val="s0">
                                    <SubDAG type="deterministic" var="rock_1" val="bad"/>
                                </Edge>
                                <Edge val="s1">
                                    <SubDAG type="persistent" var="rock_1"/>
                                </Edge>
                                <Edge val="s2">
                                    <SubDAG type="persistent" var="rock_1"/>
                                </Edge>
                            </Node>
                        </Edge>
                    </Node>
                </DAG>
            </Parameter>
        </CondProb>
    </StateTransitionFunction>
</pomdpx>
        """)
        expected_state_transition_function = \
            [{'Var': 'rover_1',
              'Parent': ['action_rover', 'rover_0'],
              'Type': 'DD',
              'Parameter': {'action_rover': {'amw': {'rover_0': {'s0': {'type': 'deterministic',
                                                                        'var': 'rover_1',
                                                                        'val': 's2'},
                                                                 's1': {'type': 'deterministic',
                                                                        'var': 'rover_1',
                                                                        'val': 's0'},
                                                                 's2': {'type': 'deterministic',
                                                                        'var': 'rover_1',
                                                                        'val': 's2'}}},
                                             'ame': {'rover_0': {'s0': {'type': 'deterministic',
                                                                        'var': 'rover_1',
                                                                        'val': 's1'},
                                                                 's1': {'type': 'deterministic',
                                                                        'var': 'rover_1',
                                                                        'val': 's2'},
                                                                 's2': {'type': 'deterministic',
                                                                        'var': 'rover_1',
                                                                        'val': 's2'},
                                                                 }},
                                             'ac': {'type': 'persistent',
                                                    'var': 'rover_1'},
                                             'as': {'rover_0': {'s0': {'type': 'deterministic',
                                                                       'var': 'rover_1',
                                                                       'val': 's0'},
                                                                's1': {'type': 'deterministic',
                                                                       'var': 'rover_1',
                                                                       'val': 's2'},
                                                                's2': {'type': 'deterministic',
                                                                       'var': 'rover_1',
                                                                       'val': 's2'}}}}}},
             {'Var': 'rock_1',
              'Parent': ['action_rover', 'rover_0', 'rock_0'],
              'Type': 'DD',
              'Parameter': {'action_rover': {'amw': {'type': 'persistent',
                                                     'var': 'rock_1'},
                                             'ame': {'type': 'persistent',
                                                     'var': 'rock_1'},
                                             'ac': {'type': 'persistent',
                                                    'var': 'rock_1'},
                                             'as': {'rover_0': {'s0': {'type': 'deterministic',
                                                                       'var': 'rock_1',
                                                                       'val': 'bad'},
                                                                's1': {'type': 'persistent',
                                                                       'var': 'rock_1'},
                                                                's2': {'type': 'persistent',
                                                                       'var': 'rock_1'}}}}}}]
        self.maxDiff = None
        self.assertEqual(self.reader.get_state_transition_function(),
                         expected_state_transition_function)

    def tearDown(self):
        del self.reader
