#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
from math import pi
import sip



class costa_loop(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "costa_loop")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.symb_rate = symb_rate = 50000
        self.sps = sps = 8
        self.t_alpha_range = t_alpha_range = 1
        self.samp_rate = samp_rate = symb_rate*sps
        self.ip_factor = ip_factor = 20
        self.freq_slider = freq_slider = 0.4
        self.Qpsk = Qpsk = [-1-1j, -1+1j,1-1j, 1+1j]
        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist(Qpsk, [0, 1, 3, 2],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.thresh = thresh = 1e-3
        self.t_alpha = t_alpha = t_alpha_range
        self.samp_rate_iq = samp_rate_iq = samp_rate*ip_factor
        self.r_alpha = r_alpha = 1
        self.ntaps = ntaps = 11*sps
        self.noise_amp = noise_amp = 0
        self.gain = gain = 3
        self.freq_offset = freq_offset = freq_slider

        ##################################################
        # Blocks
        ##################################################

        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, 'symbol vs chunk')
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, 'transmitted_signal')
        self.tab_widget_2 = Qt.QWidget()
        self.tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_2)
        self.tab_grid_layout_2 = Qt.QGridLayout()
        self.tab_layout_2.addLayout(self.tab_grid_layout_2)
        self.tab.addTab(self.tab_widget_2, 'match_filtered_sps_1')
        self.tab_widget_3 = Qt.QWidget()
        self.tab_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_3)
        self.tab_grid_layout_3 = Qt.QGridLayout()
        self.tab_layout_3.addLayout(self.tab_grid_layout_3)
        self.tab.addTab(self.tab_widget_3, 'saw_tooth_wave')
        self.tab_widget_4 = Qt.QWidget()
        self.tab_layout_4 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_4)
        self.tab_grid_layout_4 = Qt.QGridLayout()
        self.tab_layout_4.addLayout(self.tab_grid_layout_4)
        self.tab.addTab(self.tab_widget_4, 'final_output')
        self.top_layout.addWidget(self.tab)
        self._noise_amp_range = Range(0, 5, 0.1, 0, 200)
        self._noise_amp_win = RangeWidget(self._noise_amp_range, self.set_noise_amp, "'noise_amp'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_amp_win)
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_float, 1, 'tcp://127.0.0.1:50001', 100, False, (-1), True)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_float, 1, 'tcp://127.0.0.1:50001', 100, False, (-1), False)
        self._t_alpha_range_range = Range(0, 1, 0.05, 1, 200)
        self._t_alpha_range_win = RangeWidget(self._t_alpha_range_range, self.set_t_alpha_range, "'t_alpha_range'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._t_alpha_range_win)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=ip_factor,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_ccf(
                interpolation=1,
                decimation=1,
                taps=firdes.root_raised_cosine(gain,samp_rate,symb_rate,r_alpha,ntaps),
                fractional_bw=0)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccf(
                interpolation=1,
                decimation=1,
                taps=firdes.root_raised_cosine(gain,samp_rate,symb_rate,t_alpha,ntaps),
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=ip_factor,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            symb_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.tab_layout_3.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_0_1_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            symb_rate, #bw
            "", #name
            False, #plotfreq
            False, #plotwaterfall
            False, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_1_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_sink_x_0_1_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_1_0.enable_rf_freq(False)

        self.tab_layout_4.addWidget(self._qtgui_sink_x_0_1_0_win)
        self.qtgui_sink_x_0_1 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            symb_rate, #bw
            "", #name
            False, #plotfreq
            False, #plotwaterfall
            False, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_1.set_update_time(1.0/10)
        self._qtgui_sink_x_0_1_win = sip.wrapinstance(self.qtgui_sink_x_0_1.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_1.enable_rf_freq(False)

        self.tab_layout_2.addWidget(self._qtgui_sink_x_0_1_win)
        self.qtgui_sink_x_0_0 = qtgui.sink_f(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate_iq, #bw
            "", #name
            True, #plotfreq
            False, #plotwaterfall
            False, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.tab_layout_1.addWidget(self._qtgui_sink_x_0_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            symb_rate, #bw
            "", #name
            False, #plotfreq
            False, #plotwaterfall
            False, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.tab_layout_0.addWidget(self._qtgui_sink_x_0_win)
        self.low_pass_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate_iq,
                40000,
                10000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate_iq,
                40000,
                10000,
                window.WIN_HAMMING,
                6.76))
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(sps, [1])
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.iir_filter_xxx_0_0 = filter.iir_filter_ffd([1.0001,-1], [-1,1], True)
        self.iir_filter_xxx_0 = filter.iir_filter_ffd([0.01], [1,0.99], True)
        self._freq_slider_range = Range(0, 10, 0.1, 0.4, 200)
        self._freq_slider_win = RangeWidget(self._freq_slider_range, self.set_freq_slider, "'freq_slider'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_slider_win)
        self.fir_filter_xxx_0_0 = filter.fir_filter_ccf(sps, [1])
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(variable_constellation_0)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(Qpsk, 1)
        self.blocks_vco_c_0 = blocks.vco_c(symb_rate, (-5), 1)
        self.blocks_unpack_k_bits_bb_0_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_threshold_ff_0_0 = blocks.threshold_ff((-thresh), thresh, 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff((-thresh), thresh, 0)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_skiphead_1_0_0 = blocks.skiphead(gr.sizeof_char*1, 3)
        self.blocks_pack_k_bits_bb_0_0_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(2)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_multiply_xx_2_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_2_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_2 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_1_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_2_0 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff((-1))
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_ff(2)
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_ff(2)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(1.414)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1.414)
        self.blocks_float_to_complex_1_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, 'C:\\Users\\YASH\\Desktop\\Mtech stuff\\placement\\projects\\final projects\\costa loop and DM\\yash\\original_data.txt', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'C:\\Users\\YASH\\Desktop\\Mtech stuff\\placement\\projects\\final projects\\costa loop and DM\\yash\\output.txt', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 150)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff((-0.5))
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-0.5))
        self.analog_sig_source_x_0_1 = analog.sig_source_f(samp_rate_iq, analog.GR_COS_WAVE, (500000+freq_offset), 1, 0, 0)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_f(samp_rate_iq, analog.GR_SIN_WAVE, (500000+freq_offset), 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate_iq, analog.GR_COS_WAVE, 500000, 1, 0, 0)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, noise_amp, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_1_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_1_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.blocks_multiply_xx_2, 1))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.blocks_threshold_ff_0_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.blocks_multiply_xx_2_0, 1))
        self.connect((self.blocks_complex_to_real_1, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.iir_filter_xxx_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.blocks_float_to_complex_1_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_xx_2, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_multiply_xx_2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_float_to_complex_1_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_float_to_complex_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.zeromq_push_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2_0, 0), (self.blocks_vco_c_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_1_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_multiply_xx_2, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_multiply_xx_2_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_multiply_xx_2_1, 0), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.blocks_multiply_xx_2_1, 0), (self.blocks_complex_to_real_1, 0))
        self.connect((self.blocks_multiply_xx_2_1, 0), (self.qtgui_sink_x_0_1_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0_0_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_skiphead_1_0_0, 0), (self.blocks_unpack_k_bits_bb_0_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.iir_filter_xxx_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_0, 0), (self.blocks_pack_k_bits_bb_0_0_0_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.blocks_multiply_xx_2_1, 1))
        self.connect((self.blocks_vco_c_0, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_skiphead_1_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.blocks_multiply_xx_2_1, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.qtgui_sink_x_0_1, 0))
        self.connect((self.iir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.iir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.iir_filter_xxx_0_0, 0), (self.blocks_multiply_const_vxx_2_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.zeromq_pull_source_0, 0), (self.blocks_delay_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "costa_loop")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate
        self.set_samp_rate(self.symb_rate*self.sps)
        self.qtgui_sink_x_0.set_frequency_range(0, self.symb_rate)
        self.qtgui_sink_x_0_1.set_frequency_range(0, self.symb_rate)
        self.qtgui_sink_x_0_1_0.set_frequency_range(0, self.symb_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.symb_rate)
        self.rational_resampler_xxx_0_0.set_taps(firdes.root_raised_cosine(self.gain,self.samp_rate,self.symb_rate,self.t_alpha,self.ntaps))
        self.rational_resampler_xxx_0_0_0.set_taps(firdes.root_raised_cosine(self.gain,self.samp_rate,self.symb_rate,self.r_alpha,self.ntaps))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_ntaps(11*self.sps)
        self.set_samp_rate(self.symb_rate*self.sps)

    def get_t_alpha_range(self):
        return self.t_alpha_range

    def set_t_alpha_range(self, t_alpha_range):
        self.t_alpha_range = t_alpha_range
        self.set_t_alpha(self.t_alpha_range)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_rate_iq(self.samp_rate*self.ip_factor)
        self.rational_resampler_xxx_0_0.set_taps(firdes.root_raised_cosine(self.gain,self.samp_rate,self.symb_rate,self.t_alpha,self.ntaps))
        self.rational_resampler_xxx_0_0_0.set_taps(firdes.root_raised_cosine(self.gain,self.samp_rate,self.symb_rate,self.r_alpha,self.ntaps))

    def get_ip_factor(self):
        return self.ip_factor

    def set_ip_factor(self, ip_factor):
        self.ip_factor = ip_factor
        self.set_samp_rate_iq(self.samp_rate*self.ip_factor)

    def get_freq_slider(self):
        return self.freq_slider

    def set_freq_slider(self, freq_slider):
        self.freq_slider = freq_slider
        self.set_freq_offset(self.freq_slider)

    def get_Qpsk(self):
        return self.Qpsk

    def set_Qpsk(self, Qpsk):
        self.Qpsk = Qpsk
        self.digital_chunks_to_symbols_xx_0.set_symbol_table(self.Qpsk)

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0
        self.digital_constellation_decoder_cb_0.set_constellation(self.variable_constellation_0)

    def get_thresh(self):
        return self.thresh

    def set_thresh(self, thresh):
        self.thresh = thresh
        self.blocks_threshold_ff_0.set_hi(self.thresh)
        self.blocks_threshold_ff_0.set_lo((-self.thresh))
        self.blocks_threshold_ff_0_0.set_hi(self.thresh)
        self.blocks_threshold_ff_0_0.set_lo((-self.thresh))

    def get_t_alpha(self):
        return self.t_alpha

    def set_t_alpha(self, t_alpha):
        self.t_alpha = t_alpha
        self.rational_resampler_xxx_0_0.set_taps(firdes.root_raised_cosine(self.gain,self.samp_rate,self.symb_rate,self.t_alpha,self.ntaps))

    def get_samp_rate_iq(self):
        return self.samp_rate_iq

    def set_samp_rate_iq(self, samp_rate_iq):
        self.samp_rate_iq = samp_rate_iq
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate_iq)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate_iq)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate_iq)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate_iq, 40000, 10000, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate_iq, 40000, 10000, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samp_rate_iq)

    def get_r_alpha(self):
        return self.r_alpha

    def set_r_alpha(self, r_alpha):
        self.r_alpha = r_alpha
        self.rational_resampler_xxx_0_0_0.set_taps(firdes.root_raised_cosine(self.gain,self.samp_rate,self.symb_rate,self.r_alpha,self.ntaps))

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps
        self.rational_resampler_xxx_0_0.set_taps(firdes.root_raised_cosine(self.gain,self.samp_rate,self.symb_rate,self.t_alpha,self.ntaps))
        self.rational_resampler_xxx_0_0_0.set_taps(firdes.root_raised_cosine(self.gain,self.samp_rate,self.symb_rate,self.r_alpha,self.ntaps))

    def get_noise_amp(self):
        return self.noise_amp

    def set_noise_amp(self, noise_amp):
        self.noise_amp = noise_amp
        self.analog_noise_source_x_0.set_amplitude(self.noise_amp)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.rational_resampler_xxx_0_0.set_taps(firdes.root_raised_cosine(self.gain,self.samp_rate,self.symb_rate,self.t_alpha,self.ntaps))
        self.rational_resampler_xxx_0_0_0.set_taps(firdes.root_raised_cosine(self.gain,self.samp_rate,self.symb_rate,self.r_alpha,self.ntaps))

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.analog_sig_source_x_0_0_0.set_frequency((500000+self.freq_offset))
        self.analog_sig_source_x_0_1.set_frequency((500000+self.freq_offset))




def main(top_block_cls=costa_loop, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
