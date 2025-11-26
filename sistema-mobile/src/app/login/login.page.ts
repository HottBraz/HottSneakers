import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent,
  IonLabel,
  IonInput,
  IonItem,
  IonButton,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardTitle
} from '@ionic/angular/standalone';
import { LoadingController } from '@ionic/angular';
import { NavController } from '@ionic/angular';
import { AlertController } from '@ionic/angular';
import { ToastController } from '@ionic/angular';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { Storage } from '@ionic/storage-angular';
import { Usuario } from './usuario.model';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: true,
  imports: [
    IonContent,
    IonLabel,
    IonInput,
    IonItem,
    IonButton,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardTitle,
    CommonModule,
    FormsModule
  ],
  providers: [Storage]
})
export class LoginPage implements OnInit {
  
  public instancia: { username: string, password: string } = {
    username: '',
    password: ''
  };

  constructor(
    public controle_carregamento: LoadingController,
    public controle_navegacao: NavController,
    public controle_alerta: AlertController,
    public controle_toast: ToastController,
    public storage: Storage
  ) { }

  async ngOnInit() {
    await this.storage.create();
  }


  async autenticarUsuario() {

    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({message: 'Autenticando...', duration: 15000});
    await loading.present();

    // Define informações do cabeçalho da requisição
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json'
      },
      url: `${environment.apiUrl}/api/login/`,
      data: this.instancia
    };

    // Autentica usuário junto a API do sistema web
    CapacitorHttp.post(options)
      .then(async (resposta: HttpResponse) => {

        // Verifica se a requisição foi processada com sucesso
        if(resposta.status == 200) {

          // Armazena localmente as credenciais de usuário
          let usuario: Usuario = Object.assign(new Usuario(), resposta.data);
          await this.storage.set('usuario', usuario);
          
          // Finaliza autenticação e redireciona para interface inicial
          loading.dismiss();
          this.controle_navegacao.navigateRoot('/home');
        }
        else {
          // Finaliza autenticação e apresenta mensagem de erro
          loading.dismiss();
          this.apresenta_mensagem(`Falha ao autenticar usuário: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        if (erro?.status) {
          this.apresenta_mensagem(`Falha ao autenticar usuário: código ${erro.status}`);
        } else {
          this.apresenta_mensagem('Erro de conexão. Verifique se o servidor está rodando.');
        }
      });
  }

  async apresenta_mensagem(mensagem: string) {
    const toast = await this.controle_toast.create({
      message: mensagem,
      cssClass: 'ion-text-center',
      duration: 3000
    });
    toast.present();
  }
}
