import os
from rich.console import Console
from rich import pretty
from restRepositories.soilsense import FeaturesRestRepository, SessionRestRepository
import utils
import forms
from dotenv import load_dotenv
import urllib3


urllib3.disable_warnings()
load_dotenv()
pretty.install()

def main(
        featuresRestRepository: FeaturesRestRepository,
        sessionRestRepository: SessionRestRepository,
):
    # Inicia uma nova 'janela'
    window = utils.Window()

    # # Apresentação inicial
    # basics = utils.Basics()
    # window.run(basics.runPreTasks)

    authForm = forms.LoginForm(sessionRestRepository=sessionRestRepository)
    window.run(authForm.run)

    fieldForm = forms.FieldForm(featuresRestRepository=featuresRestRepository)
    window.run(fieldForm.run)

if __name__ == '__main__':
    main(
        featuresRestRepository=FeaturesRestRepository(
            base_url=os.getenv('API_SOILSENSE__BASE_URL')
        ),
        sessionRestRepository=SessionRestRepository(
            base_url=os.getenv('API_SOILSENSE__BASE_URL')
        )
    )