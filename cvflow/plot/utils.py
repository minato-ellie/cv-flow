def batched_plot(image, function, *args, **kwargs):
    """
    Plot image with batched function.

    Args:
        image: Image to plot.
        function: Function to plot image.
        *args: Positional arguments of function.
        **kwargs: Keyword arguments of function.

    Returns:
        Image with plot.
    """
    if image.ndim == 3:
        image = image[None]
    for i in range(image.shape[0]):
        image[i] = function(image[i], *args, **kwargs)
    return image
