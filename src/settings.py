class Settings:
    """Class with helpful variables to utilize
    """

    class FB:
        """Class with data for FB
        """

        URL_APPS = "https://developers.facebook.com/apps/"
        URL_ADV_APPS = "https://developers.facebook.com/apps/{}/settings/advanced/"

        class Loggining:
            """Helpful variables for get fb logged in
            """
            
            LOGIN = '+48571281464'
            PASSWORD = '2448Facebook'
            URL_LOGIN = "https://www.facebook.com/login/"

            class Auth2FA:
                """if you need to get through fb 2fa
                """
                import secrets
                URL_2FA = 'https://2fa.live/'
                SECRET_CODE = secrets.token_urlsafe(25) # temporary variable for tests

        class TagsAtribsParams:
            """tags for html hooks
            """            

            class Params:
                """html params
                """                
                APP_CLASS = '_6g3g'
                SPAN_IDS = 'div.x6s0dn4.x78zum5.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x178xt8z.xm81vs4.xso031l.xy80clv.xb9moi8.xfth1om.x21b0me.xmls85d.xhk9q7s.x1otrzb0.x1i1ezom.x1o6z2jb.x1gzqxud.x108nfp6.xm7lytj.x1ykpatu.xu0aao5.x9f619.xurb0ha.x1sxyh0.x1odjw0f.x1a02dak > div.xeuugli.x2lwn1j.x6s0dn4.x78zum5.x1q0g3np.x1iyjqo2.xozqiw3.x19lwn94 > div > div > div > span'
                INPUT_IDS = 'div.x6s0dn4.x78zum5.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x178xt8z.xm81vs4.xso031l.xy80clv.xb9moi8.xfth1om.x21b0me.xmls85d.xhk9q7s.x1otrzb0.x1i1ezom.x1o6z2jb.x1gzqxud.x108nfp6.xm7lytj.x1ykpatu.xu0aao5.x9f619.xurb0ha.x1sxyh0.x1odjw0f.x1a02dak > div.xeuugli.x2lwn1j.x6s0dn4.x78zum5.x1q0g3np.x1iyjqo2.xozqiw3.x19lwn94 > div > div > div > input'

            class XPath:
                """html xpath
                """                
                ADS_PALLETTE = '/html/body/div[1]/div[5]/div[1]/div/div[5]/div[2]/div[2]/div/div/form/div[8]/div/div/div/div[1]/div'
                SAVE_BUTTON = '/html/body/div[1]/div[5]/div[1]/div/div[5]/div[2]/div[2]/div/div/form/div[11]/div/div/div[2]/button'
                
                