# Dependencies
from selenium import webdriver, common
from Include import secrets
from time import sleep
import sys



class Profile:
    """
    This method contains the getter and setters, as well as the constructor.
    It also contains the methods that will allow us to automate the process/.
    """

    def __init__(self):  # Set diver version
        """
        This is the constructor function.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--allow-silent-push")
        options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(chrome_options = options)
        self.username = secrets.username
        self.password = secrets.password

    def GoTo(self, url_ = 'https://tinder.com'):
        self.driver.delete_all_cookies()
        self.driver.get(url_)
        sleep(1)

    def ifPopUp(self, popupId):
        """
        This function will determine if there is a pop up in the process, so we can
        hide it later.
        :param popupId:
        :return:
        """
        exist = True

        try:
            if self.driver.find_element_by_id(popupId) is not None:
                exist = True
            else:
                exist = False
        except:
            exist = False

        return exist

    def checkIfElementExists(self, elem_Xpath):
        """
        This method will allow us to check if an element exist after reloading a page
        or changing between views. That way we wont have to rely on connection speed
        and sleeps.
        The method will iterate 10 times to check for the element and it will wait a
        few second between iterations.
        :param elem_Xpath:
        :return:
        """
        isElement = False
        sleep(2.5)
        for tries in range(10):
            try:
                if self.driver.find_element_by_xpath(elem_Xpath) is not None:
                    isElement = True
                    break
            except:
                isElement = False
                sleep(1)
                continue
        return isElement

    def closeCookies(self):
        """
        This method is used just to accept the cookies.
        :return:
        """
        if self.checkIfElementExists('//*[@id="content"]/div/div[2]'):
            self.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[1]/button/span').click()

    def selectFacebookLoginMethod(self):
        """
                This method will select the Facebook login option. Since is random wether it appears or not
                and it has no absolute position, we cover our bases with all the cases we mapped.
                :return:
                """
        # In all the cases mapped, the Facebook login button will never be placed as the first one
        # So we are working under the assumption that it will be in the other two positions
        # In case the devs change this and starts throwing errors, the source code must be
        # modified

        try:
            # List of Xpaths of the other elements or buttons
            loginElemLst = self.driver.find_elements_by_xpath(
                '/html/body/div[2]/div/div/div/div/div[3]/span/div/button/span[2]')

            # if the first element of the list contains the Facebook key word, bot will click it
            if 'FACEBOOK' in loginElemLst[0].text:
                loginElemLst[0].click()

            # else if, the list only has one element, and isn't obviously the Facebook one
            elif len(loginElemLst) == 1:

                # Click the more options link and reload the list so it can get more that one element
                self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[3]/span/button').click()
                sleep(2)
                loginElemLst = self.driver.find_elements_by_xpath(
                    '/html/body/div[2]/div/div/div/div/div[3]/span/div/button/span[2]')

                # Find the index of the element that contains the Facebook keyword and add 1 since Python
                # indexing begins with 0 and Xpaths dont
                for i, elem in enumerate(loginElemLst):
                    if 'FACEBOOK' in elem.text:
                        indexFB = i + 1
                        elem.click()

            # The 3 options got shown on the screen
            else:

                # Find the index of the element that contains the Facebook keyword and add 1 since Python
                # indexing begins with 0 and Xpaths dont
                for i, elem in enumerate(loginElemLst):
                    if 'FACEBOOK' in elem.text:
                        indexFB = i + 1
                        elem.click()

        except common.exceptions.NoSuchElementException as e:
            self.driver.close()
            self.driver.quit()
            raise Exception('There was a problem with the Facebook Authentication selection /n'
                            f'Exception Message: {e.msg}')

    def login(self):
        """
        This method performs the login function.
        It will call the close cookies function
        It will call the select facebook login method function
        It will proceed to fill in the fields and finally close the pop-ups
        one Tinder is on the home screen.
        :return:
        """
        popUpId = 'modal-manager'

        if not self.checkIfElementExists('/html/body/div[2]/div/div/div/div/div[1]/h3'):
            self.driver.close()
            self.driver.quit()
            sys.exit('The landing page wasnt loaded')

        self.closeCookies()

        if self.ifPopUp(popUpId):

            self.selectFacebookLoginMethod()

            loginHandle = self.driver.window_handles[1]
            baseHandle = self.driver.window_handles[0]
            self.driver.switch_to.window(loginHandle)
            self.driver.find_element_by_id('email').send_keys(self.username)
            self.driver.find_element_by_id('pass').send_keys(self.password)
            self.driver.find_element_by_id('loginbutton').click()

            self.driver.switch_to.window(baseHandle)
            sleep(3)

            if self.checkIfElementExists('//*[@id="modal-manager"]/div/div/div/div'):
                self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()

            if self.checkIfElementExists('//*[@id="modal-manager"]/div/div/div/div'):
                self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()

            # This command will finally make the popup invisible, this is done to prevent it
            # from appearing further in the process of swiping. This fix is better than fixing
            # it inside the for loop.
            self.driver.execute_script("document.getElementById('modal-manager').style.display = 'none'")

    def swipeRight(self):

        # Check if Nav Bar exists (screen transition)
        if not self.checkIfElementExists('/html/body/div[1]/div/div[1]/div/aside/div'):
            self.driver.close()
            self.driver.quit()
            print('Tinder Home Page coulndt be loaded')

        for reps in range(50):
            if self.checkIfElementExists('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button'):
                self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button').click()
