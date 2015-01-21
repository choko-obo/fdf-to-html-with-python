from docutils.utils import new_document
from docutils.writers import html4css1
from docutils.core import publish_parts
import re

DEBUG = False
#DEBUG = True

IGNORE_ATTR = (
    "start", "class", "frame", "rules",
)
IGNORE_TAGS = (
    "div",
)



class CleanHTMLWriter(html4css1.Writer):
    """
    This docutils writer will use the CleanHTMLTranslator class below.
    """
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = CleanHTMLTranslator



class CleanHTMLTranslator(html4css1.HTMLTranslator, object):
    """
    Clean html translator for docutils system.
    """
    def _do_nothing(self, node, *args, **kwargs):
        pass

    def starttag(self, node, tagname, suffix='\n', empty=0, **attributes):
        """
        create start tag with the filter IGNORE_TAGS and IGNORE_ATTR.
        """
#        return super(CleanHTMLTranslator, self).starttag(node, tagname, suffix, empty, **attributes)
#        return "XXX%r" % tagname

        if tagname in IGNORE_TAGS:
            if DEBUG:
                print("ignore tag %r" % tagname)
            return ""
        if tagname == 'h1':
            tagname = 'h1 id="%s"' % item_name
        elif tagname == 'a':
            tagname = 'a href="%s"' % attributes['href']

        parts = [tagname]
        for name, value in sorted(attributes.items()):
            # value=None was used for boolean attributes without
            # value, but this isn't supported by XHTML.
            assert value is not None

            name = name.lower()

            if name in IGNORE_ATTR:
                continue

#            part = name
#            parts.append(part)

        if DEBUG:
            print("Tag %r - ids: %r - attributes: %r - parts: %r - self.body: %r" % (
                tagname, getattr(node, "ids", "-"), attributes, parts, self.body
            ))

        if empty:
            infix = ' /'
        else:
            infix = ''
        html = '<%s%s>%s' % (' '.join(parts), infix, suffix)
        if DEBUG:
            print("startag html: %r" % html)
        return html
    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    set_class_on_child = _do_nothing
    set_first_last = _do_nothing

    # remove <blockquote> (e.g. in nested lists)
    visit_block_quote = _do_nothing
    depart_block_quote = _do_nothing

    # set only html_body, we used in rest2html() and don't surround it with <div>
    def depart_document(self, node):

        self.html_body.extend(self.body_prefix[1:] + self.body_pre_docinfo
                              + self.docinfo + self.body
                              + self.body_suffix[:-1])
        assert not self.context, 'len(context) = %s' % len(self.context)


    #__________________________________________________________________________
    # Clean table:

    visit_thead = _do_nothing
    depart_thead = _do_nothing
    visit_tbody = _do_nothing
    depart_tbody = _do_nothing

    def visit_table(self, node):
        if docutils.__version__ > "0.10":
            self.context.append(self.compact_p)
            self.compact_p = True
        self.body.append(self.starttag(node, 'table'))

    def visit_tgroup(self, node):
        node.stubs = []

    def visit_field_list(self, node):
        super(CleanHTMLTranslator, self).visit_field_list(node)
        if "<col" in self.body[-1]:
            del(self.body[-1])

    def depart_field_list(self, node):
        self.body.append('</table>\n')
        self.compact_field_list, self.compact_p = self.context.pop()

    def visit_docinfo(self, node):
        self.body.append(self.starttag(node, 'table'))

    def depart_docinfo(self, node):
        self.body.append('</table>\n')

    #__________________________________________________________________________
    # Clean image:

    depart_figure = _do_nothing

    def visit_image(self, node):
        super(CleanHTMLTranslator, self).visit_image(node)
        if not 'alt' in node.attributes:
            node.attributes['alt']='Someone forgot to add Alt text'
        if isMoebel:
            self.body[-1] = self.body[-1].replace(' />', ''' src="%s" alt="%s" /></a></div><a href="#_" class="lightbox" id="%s"><img src="%s"></a>''' % (path + node.attributes['uri'], node.attributes['alt'], re.sub('[\W_]+', '', node.attributes['uri']), path + node.attributes['uri']))
            self.body[-1] = self.body[-1].replace('<img', '<div class="intext"><a href="#%s"><img' % re.sub('[\W_]+', '',node.attributes['uri']),1)
        else:
            self.body[-1] = self.body[-1].replace(' />', ' src="%s" alt="%s"/>' % (path + node.attributes['uri'], node.attributes['alt']))


def full(content, static_path, static_name, isEinrichtung=False, enable_exit_status=None,**kwargs):
    settings_overrides = {
        "input_encoding": "unicode",
        "doctitle_xform": False,
        "file_insertion_enabled": False,
        "raw_enabled": False,
    }
    settings_overrides.update(kwargs)
    global path
    path=static_path
    global item_name
    item_name=static_name
    global isMoebel
    isMoebel=isEinrichtung
    parts = publish_parts(
        source=content,
        writer=CleanHTMLWriter(),
        settings_overrides=settings_overrides,
        enable_exit_status=enable_exit_status,
    )
    return parts["html_body"] 
