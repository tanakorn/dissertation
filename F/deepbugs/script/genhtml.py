#!/usr/bin/python

"""A script that generate a table in html for pmc project.

Usage:

genhtml.py [tagcode]

Ouput:
/tmp/jira/[tagcode].html

Example:
genhtml.py ll
"""

import os, re, sys
import urllib
import json
from datetime import datetime


# Global variables 
# Who are the reviewers. The template here is 'fl',
# which stands for first and last initial.
WHO = ['td', 'mz', 'hg', 'tl', 'tp', 'rs']
# Shorten for systems
# SYSTEMS = {'MAPREDUCE':'mr', 'HADOOP':'ha', 'HBASE':'hb', 'CASSANDRA':'ca',
#            'HDFS':'hd', 'ZOOKEEPER':'zk', 'YARN':'ya', 'FLUME':'fl'}
SYSTEMS = {'ZOOKEEPER':'zk', 'CASSANDRA':'ca','MAPREDUCE':'mr'}
TAGCODES = ['ll', 'mc']  # Known tagcodes
# Various aspects of a issue
DESC = 'desc'  # General description
COMP = 'comp'  # Component, e.g., ipc, spec. exec.
TEST = 'test'  # Test to reproduce
FAULT = 'fault'   # Failure involved, e.g, slow disk, node crash
CODE = 'code'   # Code representing budget, e.g, ZAB-3C-3R
SPEC = 'spec'   # Checks that can catch the bug.
FIX = 'fix'   # Potential fixes
VER = 'ver' # Version issue found
POL = 'pol' # Semantical policy that we can apply to SAMC
IMPACT = 'impact'
TAX = 'tax'  # HG's taxonomy
JIRA_LINK='https://issues.apache.org/jira/browse/{id}'
SAME_SHADE_ROWS = 3  # We will alternate shading after a number of rows.


i_re = re.compile('i-(\w+)(?:-(\w+))?')

implication_list = []

#--------------------------------------
#--------- Issue Data structure -------
#--------------------------------------
class Issue(object):
    """A class that represent limplock bug."""
    def __init__(self, idstr, title):
        self.idstr = idstr
        self.title = title
        i = self.idstr.find('-')
        self.sys = self.idstr[:i]
        self.num = int(self.idstr[i+1:])
        self.reviewers = []
        self.types = []
        self.priority = 99
        # Pipeline related: static analysis and petrinet.
        self.static = False
        self.net = False
        # Notes
        self.notes = {}  # mapping from description
        self.notes[DESC] = ''
        self.notes[COMP] = ''
        self.notes[TEST] = ''
        self.notes[FAULT] = ''
        self.notes[CODE] = ''
        self.notes[SPEC] = ''
        self.notes[FIX] = ''
        self.notes[VER] = ''
        self.notes[POL] = ''
        self.notes[IMPACT] = ''
        self.notes[TAX] = ''
        self.studentnotes = ''
        self.hgnotes = ''
        self.implications = []
        # tempory variable, for parsing purpose.
        self._tmp = ''

    def isRelevant(self):
        """Return True if this bug is tagged."""
        return len(self.reviewers) > 0

    def toString(self):
        """For debugging purpose only."""
        s = ''
        s += '[%s][%s]\n' % (self.idstr, self.title)
        s += 'Reviewers: %s\n' % str(self.reviewers)
        s += 'Types: %s\n' % str(self.types)
        s += 'Priority: %d\n' % self.priority
        s += 'Desc: %s\n' % self.notes[DESC]
        s += 'Comp: %s\n' % self.notes[COMP]
        s += 'Test: %s\n' % self.notes[TEST]
        s += 'Fault: %s\n' % self.notes[FAULT]
        s += 'Code: %s\n' % self.notes[CODE]
        s += 'Spec: %s\n' % self.notes[SPEC]
        s += 'Fix: %s\n' % self.notes[FIX]
        s += 'Ver: %s\n' % self.notes[VER]
        s += 'Pol: %s\n' % self.notes[POL]
        s += 'Impact: %s\n' % self.notes[IMPACT]
        s += 'Students: %s\n' % self.studentnotes
        s += 'HG: %s\n' % self.hgnotes
        return s

    def parseTags(self, line, parser):
        # Who, types, and pipeline aspect.
        m = parser.pw.match(line)
        if m:
            tag = m.group(1)
            if tag in WHO:
                self.reviewers.append(tag)
            elif tag.lower() == 'net':
                self.net = True
            elif tag.lower() == 'static':
                self.static = True
            else:
                self.types.append(tag)
        # Priority.
        m = parser.pd.match(line)
        if m:
            self.priority = int(m.group(1))
            # So lowest priority is 1 according to the script.
            if self.priority == 0:
                self.priority = 1

        m = i_re.match(line)
        if m:
            if m.lastindex == 2 and m.group(1) == 'misc':
                self.implications.append(m.group(2))
                if m.group(2) not in implication_list:
                    implication_list.append(m.group(2))
            else:
                self.implications.append(m.group(1))
                if m.group(1) not in implication_list:
                    implication_list.append(m.group(1))

    def parseNotes(self, line):
        if line.startswith(' ' * 4):
            self._tmp += line
        if len(line.strip()) == 0:
            self.processNotes(self._tmp)
            self._tmp = ''

    def processNotes(self, note):
        if note == '':
            return
        if note.startswith(' ' * 6):
            note = note.lstrip()
            i = note.find(':')
            prefix = note[:i].lower()
            content = note[i+1:]
            if prefix in self.notes:
                self.notes[prefix] += content
            else:
                self.hgnotes += '<p> %s' % note
        elif note.startswith(' ' * 4):
            note = note.lstrip()
            i = note.find(':')
            prefix = note[:i].lower()
            content = note[i+1:]
            if prefix in self.notes:
                self.notes[prefix] += content
            else:
                self.studentnotes += '<p> %s' % note

    def getWhoSortKey(self):
        if 'hg' in self.reviewers:
            who = '1hg'
        elif 'tl' in self.reviewers:
            who = '2tl'
        else:
            who = self.reviewers[0]
        return who

    def _getImage(self, check):
        if check:
            return '<img width=15 height=15 src="check.gif">'
        return '<img width=15 height=15 src="cross.gif">'

    def getSortKey(self):
        """Sort key to show in html files.
        People should write different getSortKey method if needed be.
        """
        return '<b>%02d-%s-%s</b><br><br>M:%s<br>S:%s%05d' \
            % (self.priority, self.getWhoSortKey(), SYSTEMS[self.sys],
               self._getImage(self.net), self._getImage(self.static),
               self.num)

    def getPrintSortKey(self):
        """Sort key to show in html files.
        People should write different getSortKey method if needed be.
        """
        return '<b>%02d-%s-%s</b><br><br>M:%s<br>S:%s' \
            % (self.priority, self.getWhoSortKey(), SYSTEMS[self.sys],
               self._getImage(self.net), self._getImage(self.static))


#--------------------------------------
#--------- Parse logic ----------------
#--------------------------------------
class Parser(object):
    """A class for parsing. It has info about project tag,
    and list of systems. This should be independent of how
    we print the table."""

    def __init__ (self, tagcode, systems, jirapath):
        """Constructor.

        Params:
        - tagcode: String, e.g. 'll', 'wc'
        - systems: list of String, e.g, ['mapreduce', 'hdfs']
        """
        self.tagcode = tagcode
        self.systems = systems
        self.jirapath = jirapath
        # A bunch of regex
        self.pt = re.compile('\[(.+)\]\[(.+)\]') # For tile and description
        self.pw = re.compile('%s-([a-zA-Z]+)' % tagcode) # For who and types.
        self.pd = re.compile('%s-(\d+)' % tagcode) # For priority.

    def parseSystem(self, system):
        """This function contains the parsing logic.

        Params:
        - system: String lower case, system name, e.g. 'mapreduce'.

        Return: a dict mapping issue->issue.sortedkey.
        """
        print 'Parsing %s' % system
        filename = '%s/raw/%s.txt' % (self.jirapath, system)
        if not os.path.exists(filename):
            print '%s does not exist' % filename
            sys.exit(-1)
        rawfile = open(filename, 'r')
        issues = {}
        cur = None
        # Start parsing.
        for line in rawfile:
            m = self.pt.match(line)
            if m:
                # Reach new issue, store last limplock issue.
                if cur != None and cur.isRelevant():
                    issues[cur] = cur.getSortKey()
                idstr = m.group(1)
                title = m.group(2)
                try:
                    cur = Issue(idstr, title)
                except:
                    print 'Warning: bad form'
                    print line
                    # reset parsing
                    cur = None
            if cur != None:
                cur.parseTags(line, self)
                cur.parseNotes(line)
        # Outside for loop. Remember the last issue.
        if cur.isRelevant():
            issues[cur] = cur.getSortKey()
        return issues

    def parse(self):
        """Parse all systems.
        Return: a dict mapping issue->issue.sortedkey.
        """
        issues = {}
        for system in self.systems:
            issues.update(self.parseSystem(system))
        return issues


#--------------------------------------
#--------- Create html file -----------
#--------------------------------------
class Printer(object):
    """Printing HTML utils. The logic to different table styles
    should be here. For instance, if people want new table format,
    they will add new methods here to write different format.
    """

    def __init__(self, tagcode):
        """Constructor.

        Params:
        - tagcode: String, e.g. 'll'. Output file is /tmp/jira/ll.html.
        """
        self.tagcode = tagcode
        # Prepare output dir.
        if not os.path.exists('/tmp/jira'):
            os.system('mkdir /tmp/jira')
        os.system('cp html/* /tmp/jira/')

    def printHtml(self, issues):
        """Generate /tmp/jira/[tagcode].html.

        Params:
        - issues: a map (not sorted) from issue->issue.sortkey"""
        out = open('/tmp/jira/%s.html' % self.tagcode, 'w')
        self.printHeader(out)
        self.printTableHeader(out)
        self.printTableBody(out, issues)
        self.printFooter(out)
        out.close()

    def printHeader(self, out):
        header = '<html>\n'
        header += ' <head>\n'
        header += '  <meta>\n'
        header += '  <link rel=StyleSheet href=coffee.css type=text/css>\n'
        header += ' </head>\n'
        header += ' <body>\n'
        header += ' <table>\n'
        out.write(header)

    def printFooter(self, out):
        out.write('  </table>\n')
        out.write(' </body>\n')
        out.write('</html>\n')

    def pRowStart(self, out, i=0):
        if i == 0:
            out.write('    <tr>\n')
            return
        t = i % (2 * SAME_SHADE_ROWS)
        if t >=1 and t <= SAME_SHADE_ROWS:
            out.write('    <tr class=noshade>\n')
        else:
            out.write('    <tr class=shade>\n')

    def pRowEnd(self, out):
        out.write('    </tr>\n')

    def pCol(self, out, col):
        out.write('     <td>%s</td>\n' % col)

    def printColWidth(self, out):
        out.write('<colgroup>\n')
        out.write('<col span="1" style="width: 8%;">')  # key
        out.write('<col span="1" style="width: 18%;">')  # Title
        out.write('<col span="1" style="width: 33%;">')  # Desc
        out.write('<col span="1" style="width: 20%;">')  # Moreinfo
        out.write('</colgroup>\n')

    def printTableHeader(self, out):
        self.printColWidth(out)
        out.write('    <thead>\n');
        self.pRowStart(out);
        self.pCol(out, 'Sort Key')
        self.pCol(out, 'Title')
        self.pCol(out, 'Desc')
        self.pCol(out, 'MoreInfo')
        self.pCol(out, 'HG comment')
        self.pRowEnd(out);
        out.write('    </thead>\n');

    def printTableBody(self, out, issues):
        """Notes: for new table with different column,
        please create new method.

        Params:
        - issues: a map (not sorted) from issue->issue.sortkey"""
        out.write('   <tbody>\n')
        i = 1
        for issue, sortkey in sorted(issues.items(), key=lambda x: x[1]):
            # TODO: may be combine all of this to
            # issue.getPrintentry? 
            self.pRowStart(out, i)
            self.pCol(out, issue.getPrintSortKey())
            link = JIRA_LINK.format(id=issue.idstr)
            sysnum = '%s-%d' % (SYSTEMS[issue.sys], issue.num)
            title = '<a href=\"%s\"><font size=+1><b>%s</b></font>:'
            title += ' %s (%d)</a>'
            title = title % (link, sysnum, issue.title, i)
            self.pCol(out, title)
            desc = issue.notes[DESC]
            if len(issue.studentnotes) > 0:
                desc += '<p><b>Students:</b> %s' % issue.studentnotes
            desc = desc.strip().replace('\n', '<br/>')
            self.pCol(out, desc)
            more = ''
            if len(issue.types) > 0:
                more = '<p><b>Types:</b> %s' % ', '.join(issue.types)
            if len(issue.notes[COMP]) > 0:
                more += '<p><b>Comp:</b> %s' % issue.notes[COMP]
            if len(issue.notes[IMPACT]) > 0:
                more += '<p><b>Impact:</b> %s' % issue.notes[IMPACT]
            if len(issue.notes[TEST]) > 0:
                more += '<p><b>Test:</b> %s' % issue.notes[TEST]
            if len(issue.notes[FAULT]) > 0:
                more += '<p><b>Fault:</b> %s ' % issue.notes[FAULT]
            if len(issue.notes[CODE]) > 0:
                more += '<p><b>Code:</b> %s ' % issue.notes[CODE]
            if len(issue.notes[SPEC]) > 0:
                more += '<p><b>Spec:</b> %s' % issue.notes[SPEC]
            if len(issue.notes[FIX]) > 0:
                more += '<p><b>Fix:</b> %s' % issue.notes[FIX]
            if len(issue.notes[VER]) > 0:
                more += '<p><b>Ver:</b> %s' % issue.notes[VER]
            if len(issue.notes[POL]) > 0:
                more += '<p><b>Pol:</b> %s' % issue.notes[POL]
            self.pCol(out, more)
            hg = issue.hgnotes
            if len(issue.notes[TAX]) > 0:
                hg += '<p><b>Tax:</b> %s' % issue.notes[TAX]
            self.pCol(out, hg)
            i += 1
            self.pRowEnd(out)
        out.write('   </tbody>\n')


def main():
    if len(sys.argv) != 2:
        print 'Usage: genhtml.py jira_path'
        print 'Example:'
        print '     genhtml.py /path/to/jira'
        sys.exit(-1)
    '''
    tagcode = sys.argv[1]
    if tagcode not in TAGCODES:
        print 'Error: tagcode must be in %s' % str(TAGCODES)
        sys.exit(-1)
    '''
    jirapath = sys.argv[1]
    tagcode = 'mc'
    output = {}
    proto_list = {}
    for s in SYSTEMS.keys():
        output[s] = open("../raw/%s" % s.lower(), "w")
        proto_list[s] = []

    parser = Parser(tagcode, [s.lower() for s in SYSTEMS.keys()], jirapath)
    issues = parser.parse()

    days_fixed = []

    within_six_month = 0

    for issue in issues:
        try:
            issue.notes[CODE] = issue.notes[CODE].strip()
            if ' ' in issue.notes[CODE]:
                tok = issue.notes[CODE].split(" ")
                tok = tok[0].split("-")
            else:
                tok = issue.notes[CODE].split("-")
            if len(tok) == 4:
                del tok[1]
            c = int(tok[1][:-1])
            r = int(tok[2].rstrip()[:-1])
            if c + r == 0:
                print "Ignore %s \"%s\" (c+r=0)" % (issue.idstr, issue.notes[CODE].strip())
                continue
            elif c + r > 6:
                print "Ignore %s \"%s\" (c+r>6)" % (issue.idstr, issue.notes[CODE].strip())
                continue
            if tok[0] not in proto_list[issue.sys]:
                proto_list[issue.sys].append(tok[0])

            json_content = urllib.urlopen('http://issues.apache.org/jira/rest/api/2/issue/%s?fields=resolutiondate,created,resolution' % (issue.idstr)).read()
            json_obj = json.loads(json_content)
            #print json.dumps(json_obj, sort_keys=True, indent=4, separators=(',', ': '))
            #print json_obj['fields']['resolutiondate'], json_obj['fields']['created']
            # 2010-02-20T14:27:43.351+0000
            if json_obj['fields']['resolutiondate'] is not None:
                fixed_date = datetime.strptime(json_obj['fields']['resolutiondate'][:10], "%Y-%m-%d")
                created_date = datetime.strptime(json_obj['fields']['created'][:10], "%Y-%m-%d")
                diff = (fixed_date-created_date).days + 1
                if json_obj['fields']['resolution']['name'] != "Fixed":
                    print "Issue %s is not 'Fixed' (%s)" % (issue.idstr, json_obj['fields']['resolution']['name'])
                #elif diff == 0:
                #    print "Issue %s fixed time is 0 day" % issue.idstr
                else:
                    days_fixed.append(diff)

            #print (datetime.today() - created_date)
            if (datetime.today() - created_date).days <= 31*6:
                within_six_month = within_six_month + 1

            output[issue.sys].write("%s %d %s %d %d\n" % (SYSTEMS[issue.sys], issue.num, tok[0], c, r))
        except (ValueError, IndexError):
            print "Ignore %s \"%s\"" % (issue.idstr, issue.notes[CODE].strip())
    print implication_list, proto_list
    print "within_six_month:", within_six_month
    days_fixed = sorted(days_fixed)
    print "min_days_fixed:", min(days_fixed)
    print "max_days_fixed:", max(days_fixed)
    print "average:", sum(days_fixed)/len(days_fixed)
    print "median:", days_fixed[len(days_fixed)/2] if len(days_fixed) % 2 == 1 else (days_fixed[len(days_fixed)/2]+days_fixed[len(days_fixed)/2-1])/2

if __name__ == '__main__':
    main()
