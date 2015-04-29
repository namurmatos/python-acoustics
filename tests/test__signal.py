import numpy as np
from acoustics import Signal
import pytest

import itertools as it

#def test_operator():
    
    #n = 10000
    #fs = 5000





class TestSignal():


        
    @pytest.fixture(params=[(1, 88200, 22050), (3, 88200, 22050), (3, 88200, 44100)])
    def signal(self, request):
        return Signal(np.random.randn(request.param[0], request.param[1]), request.param[2])
    
    def test_power_spectrum(self, signal):
        
        freq, power = signal.power_spectrum()
    
    
    def test_octaves(self, signal):
        
        freq, octaves = signal.octaves()
        
    
    def test_levels(self, signal):

        times, levels = signal.levels()
        
    
    def test_leq(self, signal):
        
        #s = Signal(np.random.randn(10000), 22050)
        
        leq = signal.leq()
        
        assert(type(leq) is np.ndarray)
        
        
    ## Plot methods with arguments to test.
    #plot_methods = {'plot'                      : None,
                    #'plot_levels'               :   {
                        #'time'                  : [None, 0.125, 1.0],
                        #'method'                : ['average', 'weighting'],
                        #},
                    #'plot_octaves'              : None,
                    #'plot_third_octaves'        : None,
                    #'plot_fractional_octaves'   : {
                        #'fraction'              : [3, 6]
                        #},
                    #'plot_spectrum'             : {
                        #'N'                     : [None, 8000]
                        #},
                    #}

    #@pytest.yield_fixture
    #def plot_function_with_argument(self):
        ## This won't work with pytest. Apparently they do teardown after the yield
        ## statement and therefore don't support multiple yield statements.
        ## Using a closure doesn't help either.
        #for func, arguments in self.plot_methods.items():
            #if arguments is not None:
                #for prod in it.product(*arguments.values()):
                    #yield (func, dict(zip(arguments.keys(), prod)))
            #else:
                #yield (func, None)       
        
    #def test_plot_functions(self, signal, plot_function_with_argument):
        #func, arguments = plot_function_with_argument
        #if arguments is None:
            #getattr(signal, func)()
        #else:
            #getattr(signal, func)(**arguments)
        
    
    def test_plot(self, signal):
        signal.plot()

    def test_plot_levels(self, signal):
        signal.plot_levels()
        signal.plot_levels(method='average', time=1.0)
        signal.plot_levels(method='weighting', time=1.0)
    
    def test_plot_octaves(self, signal):
        signal.plot_octaves()
    
    def test_plot_third_octaves(self, signal):
        signal.plot_third_octaves()
    
    def test_plot_fractional_octaves(self, signal):
        signal.plot_fractional_octaves(3)
        signal.plot_fractional_octaves(6)
        signal.plot_fractional_octaves(9)
    
    def plot_power_spectrum(self, signal):
        signal.plot_power_spectrum()
    
    def test_spectrogram(self, signal):
        if signal.channels > 1:
            with pytest.raises(ValueError):
                signal.spectrogram()
        else:
            signal.spectrogram()
            
        
    
    
