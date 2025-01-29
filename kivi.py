from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from rembg import remove
from PIL import Image as PILImage, ImageEnhance
from io import BytesIO

class ImageProcessingApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # FileChooser for selecting product image
        self.filechooser_product = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg', '*.bmp'])
        self.layout.add_widget(Label(text="Select Product Image"))
        self.layout.add_widget(self.filechooser_product)

        # FileChooser for selecting background image
        self.filechooser_bg = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg', '*.bmp'])
        self.layout.add_widget(Label(text="Select Background Image"))
        self.layout.add_widget(self.filechooser_bg)

        # Button to process images
        self.process_button = Button(text="Process Image")
        self.process_button.bind(on_press=self.process_image)
        self.layout.add_widget(self.process_button)

        # Image widget to display the processed image
        self.output_image = Image(size_hint=(1, 1))
        self.layout.add_widget(self.output_image)

        return self.layout

    def remove_background(self, image_path):
        with open(image_path, 'rb') as f:
            input_image = f.read()
        removed_bg = remove(input_image)
        return PILImage.open(BytesIO(removed_bg))

    def combine_images(self, foreground, background_path):
        background = PILImage.open(background_path).convert("RGBA")
        foreground = foreground.resize(background.size, PILImage.ANTIALIAS)
        foreground = foreground.convert("RGBA")
        combined = PILImage.alpha_composite(background, foreground)
        return combined

    def adjust_brightness_contrast(self, image, brightness=1.2, contrast=1.3):
        enhancer_brightness = ImageEnhance.Brightness(image)
        image = enhancer_brightness.enhance(brightness)

        enhancer_contrast = ImageEnhance.Contrast(image)
        image = enhancer_contrast.enhance(contrast)

        return image

    def process_image(self, instance):
        # Get paths of selected product and background images
        product_image_path = self.filechooser_product.selection[0] if self.filechooser_product.selection else None
        background_image_path = self.filechooser_bg.selection[0] if self.filechooser_bg.selection else None

        if not product_image_path or not background_image_path:
            # Show error message if either image is not selected
            popup = Popup(title="Error", content=Label(text="Please select both product and background images!"),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        # Remove background and process
        foreground = self.remove_background(product_image_path)
        combined_image = self.combine_images(foreground, background_image_path)
        final_image = self.adjust_brightness_contrast(combined_image)

        # Save and display the final image
        final_image.save('output.png', format="PNG")
        self.output_image.source = 'output.png'

        # Show success message
        popup = Popup(title="Success", content=Label(text="Image Processed Successfully!"),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == "__main__":
    ImageProcessingApp().run()
