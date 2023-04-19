from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock

from streams import blocks


class HomePage(Page):
    
    subpage_types = ["contact.ContactPage"]
    
    lead_text = models.CharField(
        max_length= 140,
        blank=True,
        help_text='Subheading under the banner title',
    )

    button = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name='+',
        help_text='Select an optional page to link to',
        on_delete=models.SET_NULL,
    )
    button_text = models.CharField(
        max_length=50,
        default='Read More',
        blank=False,
        help_text='Button Text',
    )
    banner_background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        help_text='The banner background image',
        on_delete=models.SET_NULL,
    )
    body = StreamField([
        ("title", blocks.TitleBlock()),
        ("cards", blocks.CardsBlock()),
        ("cta", blocks.CallToActionBlock()),
        ("testimonial", SnippetChooserBlock(
            target_model="testimonials.Testimonial",
            template = "streams/testimonial_block.html"
        )),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("lead_text"),
        PageChooserPanel("button"),
        FieldPanel("button_text"),
        ImageChooserPanel("banner_background_image"),
        FieldPanel("body"),
    ]
class ServiceListingPage(Page):

    template = "home/service_listing_page.html"
    subtitle = models.TextField(
    blank=True,
    max_length=500,
    )
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]

    def get_context(self,request,*args,**kwargs):
        context = super().get_context(request,*args,**kwargs)
        context['services'] = ServicePage.objects.live().public()
        return context

class ServicePage(Page):
    
    description = models.TextField(
        blank=True,
        max_length=500,
    )
    internal_page = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name='+',
        help_text='Select an internal Wagtail page',
        on_delete=models.SET_NULL,
    )
    external_page = models.URLField(
        blank=True,
    )
    button_text = models.CharField(
        blank=True,
        max_length=25,
    )
    service_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        help_text='Image will be used on Service Listing Page',
        on_delete= models.SET_NULL,
    )
    

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        PageChooserPanel("internal_page"),
        FieldPanel("external_page"),
        FieldPanel("button_text"),
        ImageChooserPanel("service_image"),
    ]

    def clean(self):
        super().clean()
        if self.internal_page and self.external_page:
            raise ValidationError({
                'internal_page': ValidationError("Please only select a page OR enter an external URL"),
                'external_page': ValidationError("Please only select a page OR enter an external URL"),
            })
        
        if not self.internal_page and not self.external_page:
            raise ValidationError({
                'internal_page': ValidationError("You must select a page OR enter an external URL"),
                'external_page': ValidationError("You must select a page OR enter an external URL"),
            })
