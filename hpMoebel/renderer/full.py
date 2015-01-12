import re
from docutils.core import publish_parts, publish_doctree, publish_from_doctree
import docutils
from docutils.parsers.rst import Parser
from docutils.frontend import OptionParser
from docutils.utils import new_document
from docutils.writers import html4css1

path="moebel/testmoebel/"




# here shall be precompilers. append paths to image links so that they are all relative to /
#OR! combine whatever publish_from_doctree does with publish_parts so that publish parts can accept publish_doctree output.
# make a smaller preview.rst

#then generate preview and full for all moebels
#!/usr/bin/env python
# coding: utf-8

with open('static/head') as h:
    for line in h:
        print(line)


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

'''
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', 
'__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', 
'__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'add_meta', 'astext', 'attribution_formats', 
'attval', 'check_simple_list', 'cloak_email', 'cloak_mailto', 'content_type', 'content_type_mathml', 'depart_Text', 
'depart_abbreviation', 'depart_acronym', 'depart_address', 'depart_admonition', 'depart_attribution', 'depart_author', 
'depart_authors', 'depart_block_quote', 'depart_bullet_list', 'depart_caption', 'depart_citation',
 'depart_citation_reference', 'depart_classifier', 'depart_colspec', 'depart_compound', 'depart_contact', 'depart_container', 
 'depart_copyright', 'depart_date', 'depart_decoration', 'depart_definition', 'depart_definition_list', 
 'depart_definition_list_item', 'depart_description', 'depart_docinfo', 'depart_docinfo_item', 'depart_doctest_block', 
 'depart_document', 'depart_emphasis', 'depart_entry', 'depart_enumerated_list', 'depart_field', 'depart_field_body',
  'depart_field_list', 'depart_field_name', 'depart_figure', 'depart_footer', 'depart_footnote', 'depart_footnote_reference', 
  'depart_generated', 'depart_header', 'depart_image', 'depart_inline', 'depart_label', 'depart_legend', 'depart_line', 
  'depart_line_block', 'depart_list_item', 'depart_literal', 'depart_literal_block', 'depart_math', 'depart_math_block', 
  'depart_meta', 'depart_option', 'depart_option_argument', 'depart_option_group', 'depart_option_list', 'depart_option_list_item', 
  'depart_option_string', 'depart_organization', 'depart_paragraph', 'depart_problematic', 'depart_reference', 'depart_revision', 
  'depart_row', 'depart_rubric', 'depart_section', 'depart_sidebar', 'depart_status', 'depart_strong', 'depart_subscript', 
  'depart_subtitle', 'depart_superscript', 'depart_system_message', 'depart_table', 'depart_target', 'depart_tbody', 
  'depart_term', 'depart_tgroup', 'depart_thead', 'depart_title', 'depart_title_reference', 'depart_topic', 'depart_transition', 
  'depart_version', 'dispatch_departure', 'dispatch_visit', 'doctype', 'doctype_mathml', 'embedded_stylesheet', 'emptytag',
  'encode', 'footnote_backrefs', 'generator', 'head_prefix_template', 'is_compactable', 'lang_attribute', 'mathjax_script', 
  mathjax_url', 'optional', 'set_class_on_child', 'set_first_last', 'should_be_compact_paragraph', 'sollbruchstelle', 'starttag', 
  'stylesheet_call', 'stylesheet_link', 'unimplemented_visit', 'unknown_departure', 'unknown_visit', 'visit_Text', 'visit_abbreviation', 
  'visit_acronym', 'visit_address', 'visit_admonition', 'visit_attribution', 'visit_author', 'visit_authors', 'visit_block_quote', 
  'visit_bullet_list', 'visit_caption', 'visit_citation', 'visit_citation_reference', 'visit_classifier', 'visit_colspec', 
  'visit_comment', 'visit_compound', 'visit_contact', 'visit_container', 'visit_copyright', 'visit_date', 'visit_decoration',
   'visit_definition', 'visit_definition_list', 'visit_definition_list_item', 'visit_description', 'visit_docinfo', 
   'visit_docinfo_item', 'visit_doctest_block', 'visit_document', 'visit_emphasis', 'visit_entry', 'visit_enumerated_list',
    'visit_field', 'visit_field_body', 'visit_field_list', 'visit_field_name', 'visit_figure', 'visit_footer', 'visit_footnote', 
    'visit_footnote_reference', 'visit_generated', 'visit_header', 'visit_image', 'visit_inline', 'visit_label', 'visit_legend', 
    'visit_line', 'visit_line_block', 'visit_list_item', 'visit_literal', 'visit_literal_block', 'visit_math', 'visit_math_block',
     'visit_meta', 'visit_option', 'visit_option_argument', 'visit_option_group', 'visit_option_list', 'visit_option_list_item', 
     'visit_option_string', 'visit_organization', 'visit_paragraph', 'visit_problematic', 'visit_raw', 'visit_reference', 
     'visit_revision', 'visit_row', 'visit_rubric', 'visit_section', 'visit_sidebar', 'visit_status', 'visit_strong', 'visit_subscript', 
     'visit_substitution_definition', 'visit_substitution_reference', 'visit_subtitle', 'visit_superscript', 'visit_system_message', 
     'visit_table', 'visit_target', 'visit_tbody', 'visit_term', 'visit_tgroup', 'visit_thead', 'visit_title', 'visit_title_reference',
      'visit_topic', 'visit_transition', 'visit_version', 'words_and_spaces', 'write_colspecs', 'xml_declaration']
'''

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
            print("Tag %r - ids: %r - attributes: %r - parts: %r" % (
                tagname, getattr(node, "ids", "-"), attributes, parts
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
 		#{'ids': [], 'names': [], 'alt': 'S', 'backrefs': [], 'dupnames': [], 'uri': 'moebel/testmoebel/titel.jpg', 'classes': []}
        if self.body[-1].startswith('<img'):
            align = None

            if 'align' in node:
                # image with alignment
                align = node['align']

            elif node.parent.tagname == 'figure' and 'align' in node.parent:
                # figure with alignment
                align = node.parent['align']

            if align:
                self.body[-1] = self.body[-1].replace(' />', ' align="%s" />' % align)
        self.body[-1] = self.body[-1].replace(' />', ' src="%s" alt="%s"/>' % (path + node.attributes['uri'], node.attributes['alt']))



def rest2html(content, enable_exit_status=None, **kwargs):
    settings_overrides = {
        "input_encoding": "unicode",
        "doctitle_xform": False,
        "file_insertion_enabled": False,
        "raw_enabled": False,
    }
    settings_overrides.update(kwargs)

    parts = publish_parts(
        source=content,
        writer=CleanHTMLWriter(),
        settings_overrides=settings_overrides,
        enable_exit_status=enable_exit_status,
    )
    return parts["html_body"] 


print(rest2html(open(path + 'text.rst').read()))
#print(publish_parts(publish_from_doctree(tree), writer_name='html', reader=docutils.readers.doctree.Reader(parser_name='null')))
#print(publish_parts(open(path + 'text.rst').read(), writer_name='html')['html_body'])

with open('static/tail') as t:
    for line in t:
        print(line)
