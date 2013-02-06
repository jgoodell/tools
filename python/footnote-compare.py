import os, pdb, sys
from optparse import OptionParser as P

class Footnote(object):
    """Unicode aware object to represent a footnote insance, all text is handled as Unicode internally.

    id:    Letter value for footnote; ie. 'a','b','c'  etc
    page:  The page that the footnote appears on.
    text:  The text that comprises the footnote.
    """

    def __init__(self,id,page,text,codec="utf_8"):
        try:
            self.codec = codec.decode(codec)
            self.id = id.decode(codec)
            self.page = page.decode(codec)
            self.text = text.decode(codec)
        except UnicodeDecodeError, e:
            raise e
        except UnicodeEncodeError, e:
            raise e

    def __repr__(self):
        return "Footnote('%s')" % self.id

    def __str__(self):
        return "%s:%s" % (self.id.encode(self.codec),self.text.encode(self.codec))

    def __unicode__(self):
        return u"%s:%s" % (self.id,self.text)

    def __eq__(self,other):
        if self.text == other.text:
            return True
        else:
            return False


if __name__ == "__main__":
    p = P(description="Tool to sort footnotes by ID and page, and compare their text. Col 1 ID, Col 2 Page, Col 3 Text CSV. Unicode aware.",
          prog=os.path.basename(__file__),
          epilog="Nifty!",
          usage="%prog [options] CSV_FILE")
    p.add_option('-x','--xml',action="store_const",const=1,dest="xml",help="Write footnotes to XML for NCCN CMS upload.")
    p.add_option('-v','--verbose',action="store_const",const=1,dest="verbose",help="Verbose output for debugging CSV or looking before writing.")
    p.add_option('-c','--codec',action="store",dest="codec",help="Codec to use on footnote next for decoding to Unicode.",default="utf_8")
    p.add_option('-d','--onlydups',action="store_const",const=1,dest="duplicates",help="Only prints out duplicate footnote with different text.")
    options, args = p.parse_args()
    
    if len(args) == 1 and os.path.isfile(args[0]):
        csv_file = open(args[0],'r').readlines()
        header = csv_file[0]
        entries = csv_file[1:]

        footnote_dictionary = dict()

        #pdb.set_trace()
        for each in entries:
            id,page,text = each.split(',',2)
            if footnote_dictionary.has_key(id):
                footnote = Footnote(id,page,text,codec=options.codec)
                if footnote not in footnote_dictionary[id]:
                    footnote_dictionary[id].append(footnote)
            else:
                footnote_dictionary[id] = [Footnote(id,page,text)]

        if options.verbose:
            print("="*74)
            print("Duplicate footnotes with different text.")
            print("="*74)
            for each in footnote_dictionary.values():
                if len(each) > 1:
                    for footnote in each:
                        print(footnote)

        if options.xml:
            footnote_document = """
            <footnotes>
              %s
            </footnotes>"""
            footnote_node = """
            <footnote>
              <id>%s</id>
              <page_number>%s</page_number>
              <text><p>%s</p></text>
            </footnote>"""
            footnote_collector = ""
            keys = footnote_dictionary.keys()
            keys.sort()
            for key in keys:
                for footnote in footnote_dictionary[key]:
                    if options.duplicates and len(footnote_dictionary[key]) == 1:
                        break
                    try:
                        footnote_collector += (footnote_node % (footnote.id.encode(options.codec),
                                                                footnote.page.encode(options.codec),
                                                                footnote.text.encode(options.codec)))
                    except UnicodeDecodeError, e:
                        print("Fatal Error: codec cannot handle all footnote text: %s" % e)
                        sys.exit(1)
            footnote_document = footnote_document % footnote_collector
            print(footnote_document)
    else:
        p.print_help()
