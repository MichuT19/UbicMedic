
from rest_framework.serializers import ModelSerializer,CharField,SerializerMethodField,ImageField
from home.administrador import models
from home.cliente import models
from home.trabajador import models


class CalificacionSerializer(ModelSerializer):
    foto=ImageField(read_only=True,source='id_paciente.foto')
    cliente = SerializerMethodField()

    def get_cliente(self,obj):
        return f"{obj.id_paciente.nombre} {obj.id_paciente.apellido}"

    class Meta:
        model = models.Calificacion
        fields = ['id_paciente','cliente','id_trabajador','foto','puntuacion','comentario']

class AgendaSerializer(ModelSerializer):
    class Meta:
        model = models.Agenda
        fields = ['id_Agenda','id_trabajador','descripcion','estado']


class AgendaDetalleSerializer(ModelSerializer):
    class Meta:
        model = models.AgendaDetalle
        fields = ['id_AgendaDetalle','id_Agenda','dia_semana','hora_inicio','hora_fin']

class ReporteUsuarioSerializer(ModelSerializer):
    class Meta:
        model = models.ReporteUsuario
        fields = ['id_reporte','id_usuario_reportador','id_usuario_reportado',
                  'id_tiporeporte','motivo_reporte','fecha_reporte','estado']

class TipoReporteSerializer(ModelSerializer):
    class Meta:
        model = models.TipoReporte
        fields = ['id_tiporeporte','descripcion','estado']

class BloqueosSerializer(ModelSerializer):
    class Meta:
        model = models.Bloqueos
        fields = ['id_bloqueo','id_usuario_bloqueador','id_usuario_bloqueado','fecha_bloqueo']

class ProfesionesSerializer(ModelSerializer):
    class Meta:
        model = models.Profesiones
        fields = ['id_profesiones','descripcion','estado']

class EstadoTrabajadorSerializer(ModelSerializer):
    class Meta:
        model = models.EstadoTrabajador
        fields = ['id_estado','descripcion']

class ProfesionesxTrabajadorSerializer(ModelSerializer):
    class Meta:
        model = models.ProfesionesxTrabajador
        fields = ['id_profesionesxtrabajador','id_profesiones','id_trabajador','numero_titulo','estado']

class ClienteSerializer(ModelSerializer):
    sexodescrip=SerializerMethodField()
    paisdescrip=SerializerMethodField()
    provinciadescrip=SerializerMethodField()
    ciudaddescrip=SerializerMethodField()
    sangredescrip=SerializerMethodField()

    class Meta:
        model = models.Cliente 
        fields = ["id_cliente","cedula","nombre",
                 "apellido","fecha_nacimiento","sexo",'sexodescrip',
                 "telefono","pais",'paisdescrip',"provincia",'provinciadescrip',"ciudad",'ciudaddescrip',
                 "referencia_de_domicilio","tipo_sangre",'sangredescrip',"foto"]
    def get_sexodescrip(self,obj):
        return obj.sexo.descripcion
    def get_paisdescrip(self,obj):
        return obj.pais.nombre
    def get_provinciadescrip(self,obj):
        return obj.provincia.nombre
    def get_ciudaddescrip(self,obj):
        return obj.ciudad.nombre   
    def get_sangredescrip(self,obj):
        return obj.tipo_sangre.descripcion   

    
    
    

class ServicioSerializer(ModelSerializer):
    class Meta:
        model = models.Servicio
        fields = ["id_servicio","id_profesiones","descripcion","estado"]


# class TrabajadorSerializer(ModelSerializer):
#     class Meta:
#         model = models.Trabajador
#         fields = ['id_trabajador','id_cliente','id_tipo_trabajador','pdf_cedula','coordenadas_x','coordenadas_y','estado']       
class TrabajadorSerializer(ModelSerializer):
    cliente = SerializerMethodField()
    trabajador = CharField(read_only=True, source = 'id_tipo_trabajador.descripcion')
    estadoid = CharField(read_only=True, source = 'estado.descripcion')
    foto=ImageField(read_only=True,source='id_cliente.foto')
    profesiones = SerializerMethodField()
    puntuaciones = SerializerMethodField()
    atenciones = SerializerMethodField()

    def get_atenciones(self, obj):
        calificaciones = models.Calificacion.objects.filter(id_trabajador=obj.id_trabajador)
        return calificaciones.count()

    def get_puntuaciones(self, obj):
        calificaciones = models.Calificacion.objects.filter(id_trabajador=obj.id_trabajador)
        total_puntuacion = sum([calificacion.puntuacion for calificacion in calificaciones])
        num_calificaciones = calificaciones.count()
        
        if num_calificaciones > 0:
            average_puntuacion = total_puntuacion / num_calificaciones
            return round(average_puntuacion, 2)
        else:
            return 0 

    def get_profesiones(self, trabajador):
        profesionesxtrabajador = models.ProfesionesxTrabajador.objects.filter(id_trabajador=trabajador.id_trabajador)
        id_profesiones_list = profesionesxtrabajador.values_list('id_profesiones', flat=True)
        nombres_profesiones = []
        for id_profesion in id_profesiones_list:
            try:
                profesion = models.Profesiones.objects.get(id_profesiones=id_profesion)
                nombres_profesiones.append(profesion.descripcion)
            except models.Profesiones.DoesNotExist:
                pass
        return nombres_profesiones 
    
    def get_cliente(self,obj):
        return f"{obj.id_cliente.nombre} {obj.id_cliente.apellido}"
    
    class Meta:
        model = models.Trabajador
        fields = ['id_trabajador','cliente','id_cliente','profesiones','puntuaciones','atenciones','id_tipo_trabajador','trabajador','pdf_cedula','pdf_curriculum','latitud', 'longitud','estado','estadoid','foto']

class CitaSerializer(ModelSerializer):
    trabajador = SerializerMethodField()
    id_cliente_trabajador = SerializerMethodField()
    estadoid = CharField(read_only=True, source = 'estado.descripcion')
    cliente = SerializerMethodField()
    fotoC=ImageField(read_only=True,source='id_cliente.foto')
    fotoT=ImageField(read_only=True,source='id_trabajador.id_cliente.foto')
    class Meta:
        model = models.Cita
        fields = ['id_cita','id_trabajador','id_cliente_trabajador','trabajador','id_cliente','cliente','descripcion_motivo',
                  'fecha_creacion','fecha_inicioatencion','fecha_finatencion','fecha_confirmacion',
                  'notificacion_trabajador','notificacion_cliente','notificacion_calificacion',
                  'latitud','longitud','estado','estadoid','fotoC','fotoT'
                  ]        
    def get_cliente(self,obj):
        return f"{obj.id_cliente.nombre} {obj.id_cliente.apellido}"
    def get_trabajador(self,obj):
        return f"{obj.id_trabajador.id_cliente.nombre} {obj.id_trabajador.id_cliente.apellido}"
    def get_id_cliente_trabajador(self, obj):
        return obj.id_trabajador.id_cliente.id_cliente

class DetalleCitaSerializer(ModelSerializer):
    class Meta:
        model = models.DetalleCita
        fields = '__all__'

class EnfermedadesSerializar(ModelSerializer):
    clasificaciondeenfermedad=SerializerMethodField()
    class Meta:
        model = models.Enfermedades 
        fields = ['id_enfermedad','descripcion','id_clasificacionenfermedad','clasificaciondeenfermedad','estado'] 
    def get_clasificaciondeenfermedad(self,obj):
        return obj.id_clasificacionenfermedad.descripcion
             
            

class EnfermedadesXP(ModelSerializer):
    enfermedad = SerializerMethodField()
    idclasienfermedad= CharField(read_only=True, source = 'id_enfermedad.id_clasificacionenfermedad.idclasificacion')
    class Meta:
        model = models.EnfermedadesxPaciente   
        fields = ['id_enfermedadesxpaciente','id_enfermedad','enfermedad','idclasienfermedad','id_cliente','descripcion','estado']
    def get_enfermedad(self,obj):
        return obj.id_enfermedad.descripcion

class LoginSerializer(ModelSerializer):
    clienteL = SerializerMethodField()
    class Meta:
        model = models.Login
        fields = ['id_login','clienteL','id_cliente','usuario','contrasenia','tipo_login', 'estado']
    def get_clienteL(self,obj):
        return f"{obj.id_cliente.nombre} {obj.id_cliente.apellido}"

class ChatSerializer(ModelSerializer):
    cliente = SerializerMethodField()
    trabajador = SerializerMethodField()
    fotoC=ImageField(read_only=True,source='id_cliente.foto')
    fotoT=ImageField(read_only=True,source='id_trabajador.id_cliente.foto')
    id_cliente_trabajador = SerializerMethodField()
    class Meta:
        model = models.Chat   
        fields = ['id_chat','id_cliente','cliente','id_trabajador','id_cliente_trabajador','trabajador','fecha_creacion','ultimensaje','estado','fotoC','fotoT']
    def get_cliente(self,obj):
        return f"{obj.id_cliente.nombre} {obj.id_cliente.apellido}"
    def get_trabajador(self,obj):
        return f"{obj.id_trabajador.id_cliente.nombre} {obj.id_trabajador.id_cliente.apellido}"
    def get_id_cliente_trabajador(self, obj):
        return obj.id_trabajador.id_cliente.id_cliente
    

class ChatDetalleSerializar(ModelSerializer):
    class Meta:
        model = models.ChatDetalle  
        fields = ['id_chatdetalle','id_chat','id_cliente']

class MensajeSerializar(ModelSerializer):
    class Meta:
        model = models.Mensaje  
        fields = ['id_mensaje','id_chat','id_cliente','fecha_envio',
                  'Mensaje','visto_emisor','visto_receptor','tipo_mensaje','estado_tipo']
        
class TipoSangreSerializer(ModelSerializer):
    class Meta:
        model = models.TipoSangre 
        fields = ['id_tiposangre','descripcion'] 

class PaisSerializer(ModelSerializer):   
    class Meta:
        model = models.Pais
        fields = ['id_pais','nombre']

class ProvinciaSerializer(ModelSerializer):   
    class Meta:
        model = models.Provincia
        fields = ['id_provincia','nombre','id_pais']

class CiudadSerializer(ModelSerializer):   
    class Meta:
        model = models.Ciudad
        fields = ['id_ciudad','nombre','provincia']                

class SexoSerializar(ModelSerializer):
    class Meta:
        model = models.Sexo
        fields = ['id_sexo','descripcion']