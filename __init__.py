# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RoundKoord
                                 A QGIS plugin
 round coodinates
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-03-02
        copyright            : (C) 2022 by axinav
        email                : axinav
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load RoundKoord class from file RoundKoord.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .round_koord import RoundKoord
    return RoundKoord(iface)
