

def contexts():
    def currentLanguage():
        """
            this template filter returns users current language
        """
        return request.current_language

    def renderLogo(mode='dark'):
        if mode == 'light':
            return "media/logo/logo-light.webp"
        elif mode == 'dark':
            return "media/logo/logo.webp"
        elif mode == 'dark-bg':
            return "media/logo/logo-bg.webp"
        elif mode == 'light-bg':
            return "media/logo/logo-light-bg.webp"

    def getnewsLetterForm():
        """this context return a newsletter form"""
        return NewsLetterForm()
    def getContactUsForm():
        """this context return a ContactUsForm"""
        return ContactUsForm()

    def getShopURL():
        return current_app.config.get("SHOP_URL")


    ctx = {
        "renderLogo": renderLogo,
        "currentLanguage": currentLanguage,
        "newsLetterForm": getnewsLetterForm,
        "ContactUsForm": getContactUsForm,
        "ShopURL": getShopURL,
    }
    return ctx


def StorageUrl(path: str):
    """This template filter generate dynamic urls base of app.debug mode for serving via flask or nginx
        if debug mode this filter redirect  users to flask.serve function
        but in production mode this filter redirect users to serve static via nginx
    """
    if path[0] == "/":
        path = path[1:]

    if current_app.config.get("DEBUG"):
        return url_for("web.ServeStorageFiles", path=path, _external=True)  # flask serve
    else:
        return f"/Storage/{path}"  # Nginx Serve Files


templatesFilters = {
    "StorageUrl": StorageUrl
}
