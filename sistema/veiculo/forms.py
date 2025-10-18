from django.forms import ModelForm
from veiculo.models import Veiculo

class FormularioVeiculo(ModelForm):

    """ 
    formulario para o modelo Veiculo
    """

    class Meta:
        model = Veiculo
        exclude = []