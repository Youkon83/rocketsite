from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.core import blocks as wagatil_blocks
from streams import blocks

class FlexPage(Page):
    
    body = StreamField([
        ("title", blocks.TitleBlock()),
        ("cards", blocks.CardsBlock()),
        ("cta", blocks.CallToActionBlock()),
        ("testimonial", SnippetChooserBlock(
            target_model="testimonials.Testimonial",
            template = "streams/testimonial_block.html"
        )),
        ("richtext", wagatil_blocks.RichTextBlock())
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    class Meta:
        verbose_name = "Flex (misc) Page"
        verbose_name_plural = "Flex (misc) Pages"
