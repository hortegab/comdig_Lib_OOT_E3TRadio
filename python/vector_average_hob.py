#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class vector_average_hob(gr.sync_block):
    """
    clase del bloque vector_averager_hob en gnuradio que permite promediar los vectores que va recibiendo a medida que se invoca. Hecha por Homero Ortega Boada, en la Universidad Industrial de Santander, Colombia. Contacto: homero.ortega@radiogis.uis.edu.co
Los parametros usados son:
N:        Es el tamano del vector
Nensayos: Es el umbral que limita el numero maximo de promedios correctamente realizados. Cuando a la funcion se le ha invocado un numero de veces mayor a Nensayos, el promedio continua realizandose, pero considerando que el numero de promedios realizado hasta el momento ya no se incrementa y igual a Nensayos. 
    """

    def __init__(self, N, Nensayos):
        self.N=N
        self.Nensayos=numpy.uint64=Nensayos
        self.med=numpy.empty(N,dtype=numpy.float64)
        self.count=numpy.uint64=0
    
        gr.sync_block.__init__(self, name="vector_average_hob", in_sig=[(numpy.float32, N)], out_sig=[(numpy.float32, N)])

    def work(self, input_items, output_items):
        in0 = input_items[0][0, :]
        # Nota: originalmente habíamos usado in0 = input_items[0], como en muchos otros bloques
        # pero no funció, pues en nuestro caso estamos realizando operaciones vectoriales de vectores
        # contra otros vectores. Es entonces cuando se revela una cualidad de la entrada input_items
        # y es que lo que uno creería que es un vector de N valores, pero es realmente una matriz
        # de M vectores o filas, cada uno de N valores. Lo que nos interesa está en el vector M=0
        # 1) creo que hay que probar que hay en las otras filas de la matriz, de pronto son otras partes de la misma senal
        # osea, es posible que toda la matriz sea de una sola senal vectorial, algo así como un conjunto de trenes
        # 2) probara a agregar una salida que bote cuantas funciones muestras se ha procesado hasta el momento 
        # 3) probar si se puede quitar el for haciendo esto:
        # self.med = self.med*(self.count-1)/self.count+in0/self.count. hay que probar eso primero en python
        # print(in0.shape)
        out = output_items[0]
        # <+signal processing here+>
        if self.count < self.Nensayos:
            self.count += 1	
        for i in range(0,self.N):
            self.med[i] = self.med[i]*(self.count-1)/self.count+in0[i]/self.count
        out[:]=self.med

        return len(output_items[0])

