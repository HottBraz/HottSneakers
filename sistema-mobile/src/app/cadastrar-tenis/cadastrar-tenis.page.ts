import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent,
  IonHeader,
  IonTitle,
  IonToolbar,
  IonButtons,
  IonBackButton,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardTitle,
  IonItem,
  IonLabel,
  IonInput,
  IonSelect,
  IonSelectOption,
  IonButton,
  IonIcon
} from '@ionic/angular/standalone';
import { LoadingController, NavController, ToastController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
import { environment } from '../../environments/environment';
import { Usuario } from '../login/usuario.model';
import { addIcons } from 'ionicons';
import { camera } from 'ionicons/icons';

@Component({
  selector: 'app-cadastrar-tenis',
  templateUrl: './cadastrar-tenis.page.html',
  styleUrls: ['./cadastrar-tenis.page.scss'],
  standalone: true,
  imports: [
    IonContent,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonButtons,
    IonBackButton,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardTitle,
    IonItem,
    IonLabel,
    IonInput,
    IonSelect,
    IonSelectOption,
    IonButton,
    IonIcon,
    CommonModule,
    FormsModule
  ],
  providers: [Storage]
})
export class CadastrarTenisPage implements OnInit {

  public usuario: Usuario = new Usuario();
  public tenis: any = {
    marca: null,
    modelo: '',
    tamanho: null,
    cor: null,
    tipo: null,
    foto: null
  };

  public fotoPreview: string | null = null;

  public marcas = [
    { id: 1, nome: 'NIKE' },
    { id: 2, nome: 'ADIDAS' },
    { id: 3, nome: 'PUMA' },
    { id: 4, nome: 'REEBOK' },
    { id: 5, nome: 'NEW BALANCE' },
    { id: 6, nome: 'VANS' },
    { id: 7, nome: 'CONVERSE' },
    { id: 8, nome: 'ASICS' },
    { id: 9, nome: 'MIZUNO' },
    { id: 10, nome: 'OLYMPIKUS' }
  ];

  public cores = [
    { id: 1, nome: 'VERMELHO' },
    { id: 2, nome: 'BRANCO' },
    { id: 3, nome: 'AZUL' },
    { id: 4, nome: 'PRETO' },
    { id: 5, nome: 'CINZA' },
    { id: 6, nome: 'AMARELO' }
  ];

  public tipos = [
    { id: 1, nome: 'CASUAL' },
    { id: 2, nome: 'ESPORTIVO' },
    { id: 3, nome: 'CORRIDA' },
    { id: 4, nome: 'SKATISTA' }
  ];

  constructor(
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController
  ) {
    addIcons({ camera });
  }

  async ngOnInit() {
    await this.storage.create();
    const registro = await this.storage.get('usuario');
    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
    } else {
      this.controle_navegacao.navigateRoot('/login');
    }
  }

  selecionarFoto() {
    console.log('Botão de foto clicado!');
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.style.display = 'none';
    
    input.onchange = (event: any) => {
      console.log('Arquivo selecionado');
      const file = event.target.files?.[0];
      if (file) {
        console.log('Lendo arquivo:', file.name);
        const reader = new FileReader();
        reader.onload = (e: any) => {
          console.log('Arquivo carregado com sucesso');
          this.fotoPreview = e.target.result;
          this.tenis.foto = e.target.result;
          this.apresenta_mensagem('Foto selecionada com sucesso!');
        };
        reader.onerror = (error) => {
          console.error('Erro ao ler arquivo:', error);
          this.apresenta_mensagem('Erro ao ler arquivo');
        };
        reader.readAsDataURL(file);
      }
    };
    
    document.body.appendChild(input);
    input.click();
    setTimeout(() => document.body.removeChild(input), 100);
  }

  async salvarTenis() {
    // Validação básica
    if (!this.tenis.marca || !this.tenis.modelo || !this.tenis.tamanho || !this.tenis.cor || !this.tenis.tipo) {
      this.apresenta_mensagem('Por favor, preencha todos os campos');
      return;
    }

    const loading = await this.controle_carregamento.create({ message: 'Salvando...', duration: 30000 });
    await loading.present();

    // Prepara dados com tipos corretos
    const dadosEnvio: any = {
      marca: parseInt(this.tenis.marca),
      modelo: this.tenis.modelo,
      tamanho: parseInt(this.tenis.tamanho),
      cor: parseInt(this.tenis.cor),
      tipo: parseInt(this.tenis.tipo)
    };

    // NOTA: Upload de foto será implementado em versão futura
    // Por enquanto, não envia foto para evitar erro 400
    console.log('Dados enviados para criar:', dadosEnvio);

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/tenis/api/criar/`,
      data: dadosEnvio
    };

    CapacitorHttp.post(options)
      .then(async (resposta: HttpResponse) => {
        loading.dismiss();
        if (resposta.status == 201) {
          this.apresenta_mensagem('Tênis cadastrado com sucesso!');
          this.controle_navegacao.navigateBack('/home');
        } else {
          this.apresenta_mensagem(`Falha ao cadastrar tênis: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao cadastrar tênis: ${erro?.message || 'Erro desconhecido'}`);
      });
  }

  async apresenta_mensagem(texto: string) {
    const mensagem = await this.controle_toast.create({
      message: texto,
      cssClass: 'ion-text-center',
      duration: 2000
    });
    mensagem.present();
  }
}
