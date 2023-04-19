from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList


class TitleBlock(blocks.StructBlock):
    text= blocks.CharBlock(
        required=True,
        help_text="Text to display",
    )

    class Meta:
        template= "streams/title_block.html"
        icon= "edit"
        label= "Title"
        help_text= "Centered text to display on the page"
class LinkValue(blocks.StructValue):

    def url(self) -> str:
        internal_page = self.get("internal_page")
        external_link = self.get("external_link")
        if internal_page:
            return internal_page.url
        elif external_link:
            return external_link
        return ""
    

class Link(blocks.StructBlock):
    link_text = blocks.CharBlock(
        max_length=50, 
        default="More Details"
    )
    internal_page = blocks.PageChooserBlock(
        required=False
    )
    external_link = blocks.URLBlock(
        required=False
    )
    class Meta:
        value_class = LinkValue

    def clean(self,value):
        internal_page = value.get("internal_page")
        external_link = value.get("external_link")
        errors  = {}
        if internal_page and external_link:
            errors["internal_page"] = ErrorList(["Both of these fields cannot be filled"])
            errors["external_link"] = ErrorList(["Both of these fields cannot be filled"])
        if errors:
            raise ValidationError("Validation Error", params=errors)

        return super().clean(value)
    
class Card(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=100, 
        help_text="Title text for card, max length 100 chars"
        )
    text = blocks.TextBlock(
        max_length=255, 
        help_text="Optional text for card, max length 255 chars", 
        required=False
        )
    image = ImageChooserBlock(
        help_text="Image will automatically be cropped to 570x370"
        )
    link = Link()

class CardsBlock(blocks.StructBlock):

    cards = blocks.ListBlock(
        Card()
    )

    class Meta:
        template="streams/cards_block.html"
        icon= "image"
        label = "Standard Cards"


class CallToActionBlock(blocks.StructBlock):

    title = blocks.CharBlock(max_length=200, help_text= "Max length 200 chars")
    link = Link()   

    class Meta:

        template = "streams/call_to_action_block.html"
        icon = "Plus"
        label = "Call to Action"