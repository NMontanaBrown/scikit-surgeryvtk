#coding=utf-8
import logging
import vtk

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

#pylint:disable = invalid-name, no-member
class VTKCornerAnnotation:
    """
    Wrapper for vtkCornerAnnotaiton class.
    
    """

    def __init__(self):

        self.text_actor = vtk.vtkCornerAnnotation()

        for i in range(4):

            self.text_actor.SetText(i, str(i))

    def set_text(self, text_list):
        """Set the text in each of the four corners
        
        :param text_list: Text to display, clockwise from top-left.
        :type text_list: List of 4 strings.
        """
        
        self.validate_input(text_list)

        for idx, item in enumerate(text_list):
            self.text_actor.SetText(idx, item)

    def validate_input(self, text_list):
        """Check that the text_list input is a list of four strings.
        
        :param text_list: input to check.
        """

        if not isinstance(text_list, list):
            raise TypeError('text_list is not a list')

        if not len(text_list) == 4:
            raise ValueError('Incorrect number of elements in text_list')

        for idx, item in enumerate(text_list):
            if not isinstance(item, str):
                raise ValueError('Item at position {} is not a string'.format(idx))


class VTKTextBase:
    """
    Wrapper around vtkTextActor class to set position,
    colour, size etc.
    """

    def set_text_string(self, text):
        """ 
        Set the text string.
        :param text: text to display."""
        self.validate_text_input(text)
        self.text_actor.SetInput(text)

    def set_text_position(self, x, y):
        """ 
        Set the x,y coordinates of the text (bottom-left)
        :param x: x location in pixels
        :param y: y locaiton in pixels
        """
        if self.validate_x_y_inputs(x, y):
            self.text_actor.SetPosition(x, y)

            self.x = x
            self.y = y

    def set_font_size(self, size):
        """
        Set the font size.
        :param size: size in points"""
        self.text_actor.GetTextProperty().SetFontSize(size)

    def set_colour(self, r, g, b):
        """
        Set the text colour.
        :param r: Red (0.0 - 1.0)
        :param g: Green (0.0 - 1.0)
        :param b: Blue (0.0 - 1.0)
        """
        self.text_actor.GetTextProperty().SetColor(r, g, b)

    def validate_text_input(self, text):
        """ 
        Check text input is a valid string.
        :param text: Input to validate. """

        if isinstance(text, str):
            return True

        raise TypeError('Text input to VTKText is not a string.')

    def validate_x_y_inputs(self, x, y):
        """
        Check that coordinate inputs are valid.
        :param x: x location.
        :param y: y location """
        
        valid_types = (int, float)

        if not isinstance(x, valid_types):
            raise TypeError('x input to VTKText is not a valid number')

        if not isinstance(y, valid_types):
            raise TypeError('y input to VTKText is not a valid number')

        return True


class VTKText(VTKTextBase):

    """
    VTKText object that can be placed following a left click event.
    Text will rescale if the window resizes, to try and maintain relative
    positioning.

    :param text: text to display.
    :param    x: x position (pixels)
    :param    y: y position (pixels)
    :param font_size: Font size
    param colour: Colour, RGB tuple

    """

    def __init__(self, text, x, y, font_size=24, colour=(1.0, 0, 0)):
        """ Create a VTK text actor.
        """

        self.text_actor = vtk.vtkTextActor()
        self.text_actor.SetTextScaleModeToViewport()

        self.set_text_string(text)
        self.set_text_position(x,y)
        self.set_font_size(font_size)

        r, g, b = colour
        self.set_colour(r, g, b)

    def set_parent_window(self, parent_window):
        """
        Link the object to a VTKOverlayWindow
        and set up callbacks.
        :param parent_window: VTKOverlayWindow
        """
        self.parent_window = parent_window
        self.calculate_relative_position_in_window()
        self.add_window_resize_observer()

    def calculate_relative_position_in_window(self):
        """
        Calculate position relative to the size of the screen.
        Can then be used to re-set the position if the window is
        resized.
        """

        width, height = self.parent_window.GetRenderWindow().GetSize()
        self.x_relative = self.x/width
        self.y_relative = self.y/height

    def add_window_resize_observer(self):
        """ 
        Add an observer for window resize events.
         """
        #pylint:disable=line-too-long
        self.parent_window.AddObserver('ModifiedEvent', self.callback_update_position_in_window)

    def callback_update_position_in_window(self, obj, ev):
        """ 
        Callback to set the text position when the window is resized.
        """
        #pylint:disable=unused-argument
        width, height = self.parent_window.GetRenderWindow().GetSize()

        x = self.x_relative * width
        y = self.y_relative * height

        self.set_text_position(x, y)

class VTKLargeTextCentreOfScreen(VTKTextBase):
    """
    Display large text in the centre of the screen.
    Useful for error messages/warnings etc.

    :param text: text to display.
    :param parent_window: VTKOverlayWindow that message will
                          be displayed in.
    """

    def __init__(self, text, parent_window):

        self.text_actor = vtk.vtkTextActor()
        self.text_actor.SetTextScaleModeToViewport()

        self.parent_window = parent_window

        self.set_text_string(text)
        self.calculate_text_size(None, None)

        self.add_window_resize_observer()

    def calculate_text_size(self, obj, ev):
        """
        Calculate the position and size of the text.
        Text should span the central third (x & y) of the window.
        
        """

        window_dims = self.parent_window.GetRenderWindow().GetSize()

        x = window_dims[0] // 3
        y = window_dims[1] // 3

        self.set_text_position(x,y)

        #self.text_actor.SetConstrainedFontSize(self.parent_window.GetRenderWindow(), self.x, self.y)

    def add_window_resize_observer(self):
        """ 
        Add an observer for window resize events.
         """
        #pylint:disable=line-too-long
        self.parent_window.AddObserver('ModifiedEvent', self.calculate_text_size)



