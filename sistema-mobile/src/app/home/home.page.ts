import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonContent, IonHeader, IonTitle, IonToolbar, LoadingController, NavController, ToastController, IonButtons, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonList, IonItem, IonLabel, IonIcon, IonButton, IonSearchbar, IonFab, IonFabButton } from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Tenis } from './tenis.model';
import { Usuario } from '../login/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { environment } from '../../environments/environment';
import { addIcons } from 'ionicons';
import {
  logOutOutline,
  carOutline,
  searchOutline,
  pencil,
  trash,
  add
} from 'ionicons/icons';

@Component({
  standalone: true,
  selector: 'app-tenis',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
  imports: [IonLabel, IonItem, IonList, IonCardContent, IonCardTitle, IonCardHeader, IonCard, IonButtons, IonContent, IonHeader, IonTitle, IonToolbar, IonIcon, IonButton, IonSearchbar, IonFab, IonFabButton, CommonModule, FormsModule],
  providers: [Storage]
})
export class TenisPage implements OnInit {

  public usuario: Usuario = new Usuario();
  public lista_tenis: Tenis[] = [];
  public lista_tenis_completa: Tenis[] = [];
  public termo_pesquisa: string = '';

  constructor(
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController
  ) {
    // Registra os ícones
    addIcons({ logOutOutline, carOutline, searchOutline, pencil, trash, add });
  }

  async ngOnInit() {

    // Verifica se existe registro de configuração para o último usuário autenticado
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      this.consultarTenisSistemaWeb();
    }
    else {
      this.controle_navegacao.navigateRoot('/login');
    }
  }

  async consultarTenisSistemaWeb() {

    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({ message: 'Pesquisando...', duration: 60000 });
    await loading.present();

    // Define informações do cabeçalho da requisição
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/tenis/api/listar/`
    };

    CapacitorHttp.get(options)
      .then(async (resposta: HttpResponse) => {

        // Verifica se a requisição foi processada com sucesso
        if (resposta.status == 200) {
          this.lista_tenis = resposta.data;
          this.lista_tenis_completa = resposta.data;

          // Finaliza interface com efeito de carregamento
          loading.dismiss();
        }
        else {

          // Finaliza autenticação e apresenta mensagem de erro
          loading.dismiss();
          this.apresenta_mensagem(`Falha ao consultar tênis: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao consultar tênis: código ${erro?.status}`);
      });
  }

  async excluirTenis(id: number) {

    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({ message: 'Excluindo...', duration: 30000 });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/tenis/api/deletar/${id}/`
    };

    CapacitorHttp.delete(options)
      .then(async (resposta: HttpResponse) => {

        // Verifica se a requisição foi processada com sucesso
        if (resposta.status == 204) {

          // Finaliza interface com efeito de carregamento
          loading.dismiss();
        }
        else {

          // Finaliza autenticação e apresenta mensagem de erro
          loading.dismiss();
          this.apresenta_mensagem(`Falha ao excluir o tênis: código ${resposta.status}`);
        }
      }).catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao excluir o tênis: código ${erro?.status}`);
      })
      .finally(() => {

        // Consulta novamente a lista de tênis
        this.lista_tenis = [];
        this.consultarTenisSistemaWeb();
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

  async logout() {
    await this.storage.clear();
    this.controle_navegacao.navigateRoot('/login');
  }

  pesquisar() {
    const termo = this.termo_pesquisa.toLowerCase().trim();
    
    if (!termo) {
      this.lista_tenis = this.lista_tenis_completa;
      return;
    }

    this.lista_tenis = this.lista_tenis_completa.filter(tenis => 
      tenis.nome_marca.toLowerCase().includes(termo) ||
      tenis.modelo.toLowerCase().includes(termo) ||
      tenis.tamanho.toString().includes(termo) ||
      tenis.nome_cor.toLowerCase().includes(termo) ||
      tenis.nome_tipo.toLowerCase().includes(termo)
    );

    if (this.lista_tenis.length === 0) {
      this.apresenta_mensagem('Nenhum tênis encontrado');
    }
  }

  limparPesquisa() {
    this.termo_pesquisa = '';
    this.lista_tenis = this.lista_tenis_completa;
  }

  adicionarTenis() {
    this.controle_navegacao.navigateForward('/cadastrar-tenis');
  }

  editarTenis(id: number) {
    this.controle_navegacao.navigateForward(`/editar-tenis/${id}`);
  }
}