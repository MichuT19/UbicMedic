from rest_framework.viewsets import ModelViewSet
from home.administrador import models
from home.cliente import models
from home.trabajador import models
from home.api import serializers
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice

from rest_framework.views import APIView
from rest_framework.response import Response

class CalificacionApi(ModelViewSet):
    queryset = models.Calificacion.objects.all()
    serializer_class = serializers.CalificacionSerializer

class AgendaApi(ModelViewSet):
    queryset = models.Agenda.objects.all()
    serializer_class = serializers.AgendaSerializer

class AgendaDetalleApi(ModelViewSet):
    queryset = models.AgendaDetalle.objects.all()
    serializer_class = serializers.AgendaDetalleSerializer

class ReporteUsuarioApi(ModelViewSet):
    queryset = models.ReporteUsuario.objects.all()
    serializer_class = serializers.ReporteUsuarioSerializer

class TipoReporteApi(ModelViewSet):
    queryset = models.TipoReporte.objects.all()
    serializer_class = serializers.TipoReporteSerializer

class BloqueosApi(ModelViewSet):
    queryset = models.Bloqueos.objects.all()
    serializer_class = serializers.BloqueosSerializer

class AgendaDetalleApi(ModelViewSet):
    queryset = models.AgendaDetalle.objects.all()
    serializer_class = serializers.AgendaDetalleSerializer

class ProfesionesApi(ModelViewSet):
    queryset = models.Profesiones.objects.all()
    serializer_class = serializers.ProfesionesSerializer

class EstadoTrabajadorApi(ModelViewSet):
    queryset = models.EstadoTrabajador.objects.all()
    serializer_class = serializers.EstadoTrabajadorSerializer

class ServiciosApi(ModelViewSet):
    queryset = models.Servicio.objects.all()
    serializer_class = serializers.ServicioSerializer     

class ClienteApi(ModelViewSet):
    queryset = models.Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

class TrabajadorApi(ModelViewSet):
    queryset = models.Trabajador.objects.all()
    serializer_class = serializers.TrabajadorSerializer

class CitaApi(ModelViewSet):
    queryset = models.Cita.objects.all()
    serializer_class = serializers.CitaSerializer

    def perform_create(self, serializer):
        #cita registrada
        cita = serializer.save()
        user = cita.id_trabajador.id_cliente
        cliente = models.Login.objects.get(id_cliente=user)
        persona= cliente.usuario
        device = FCMDevice.objects.get(name = persona)
        print("dispositivo")
        print(device)
        device.send_message(Message(notification=Notification(title='Nueva cita', body='Se ha resgistrado una nueva cita')))

    def perform_update(self, serializer):
        cita = serializer.save()
        user = cita.id_cliente
        cliente = models.Login.objects.get(id_cliente=user)
        persona= cliente.usuario
        device = FCMDevice.objects.get(name = persona)
        if cita.estado.descripcion == "Aceptada":
            device.send_message(Message(notification=Notification(title='Cita aceptada', body='Tu cita ha sido aceptada')))
        else:
            device.send_message(Message(notification=Notification(title='Cita rechazada', body='Tu cita ha sido rechazada')))  


class DetalleCitaApi(ModelViewSet):
    queryset = models.DetalleCita.objects.all()
    serializer_class = serializers.DetalleCitaSerializer


class ProfesionesxTrabajadorApi(ModelViewSet):
    queryset = models.ProfesionesxTrabajador.objects.all()
    serializer_class = serializers.ProfesionesxTrabajadorSerializer  

class EnfermedadesApi(ModelViewSet): 
    queryset = models.Enfermedades.objects.all()
    serializer_class = serializers.EnfermedadesSerializar

class EmfermedadesxPacienteApi(ModelViewSet):  
    queryset = models.EnfermedadesxPaciente.objects.all()
    serializer_class = serializers.EnfermedadesXP


class LoginApi(ModelViewSet):
    queryset = models.Login.objects.all()
    serializer_class = serializers.LoginSerializer 

class MensajeApi(ModelViewSet):
    queryset = models.Mensaje.objects.all()
    serializer_class = serializers.MensajeSerializar

    def perform_create(self, serializer):
        #cita registrada
        mensaje = serializer.save()
        emisor = mensaje.id_cliente
        usuario1 = mensaje.id_chat.id_cliente
        usuario2 = mensaje.id_chat.id_trabajador.id_cliente
        
        if usuario1 != emisor:  
                cliente = models.Login.objects.get(id_cliente=usuario1)
        else:
                cliente = models.Login.objects.get(id_cliente=usuario2)
            
        persona = cliente.usuario
            
        try:
                device = FCMDevice.objects.get(name=persona)
                device.send_message(Message(notification=Notification(title='Nuevo mensaje', body=f'{mensaje.Mensaje}'),
                                            data={
        "Nick" : "Mario",
        "body" : "great match!",
        "Room" : f'{mensaje.id_cliente}'
   }))
                
        except FCMDevice.DoesNotExist:
                print("No se encontró un dispositivo registrado para el usuario:", persona)

class ChatApi(ModelViewSet):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer

class ChatDetalle(ModelViewSet):
    queryset = models.ChatDetalle.objects.all()
    serializer_class = serializers.ChatDetalleSerializar  

class TipoSangreApi(ModelViewSet):
    queryset = models.TipoSangre.objects.all()
    serializer_class = serializers.TipoSangreSerializer

class PaisApi(ModelViewSet):
    queryset = models.Pais.objects.all()
    serializer_class = serializers.PaisSerializer

class ProvinciaApi(ModelViewSet):
    queryset = models.Provincia.objects.all()
    serializer_class = serializers.ProvinciaSerializer

class CiudadApi(ModelViewSet):
    queryset = models.Ciudad.objects.all()
    serializer_class = serializers.CiudadSerializer   

class SexoApi(ModelViewSet):
    queryset = models.Sexo.objects.all()
    serializer_class = serializers.SexoSerializar

import secrets

class ObtenerToken(APIView):
    def post(self, request, *args, **kwargs):
        usuario = request.data.get('usuario')
        contrasenia = request.data.get('contrasenia')

        try:
            cliente = models.Login.objects.get(usuario=usuario)
        except models.Login.DoesNotExist:
            return Response({"error": "Credenciales inválidas."}, status=400)

        if cliente.contrasenia == contrasenia:
            try:
                token = models.CustomToken.objects.get(login=cliente)
            except models.CustomToken.DoesNotExist:
                token = models.CustomToken(login=cliente, key=secrets.token_hex(16))
                token.save()
                
            return Response({'token': token.key})
        else:
            return Response({"error": "Contraseña inválidas."}, status=400)    