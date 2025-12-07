import onnxruntime
import numpy as np
import os

class SileroVAD:
    def __init__(self, model_path, threshold=0.5):
        self.session = onnxruntime.InferenceSession(model_path)
        self.reset_states()
        self.threshold = threshold
        self.sample_rate = 16000

    def reset_states(self):
        self._h = np.zeros((2, 1, 64)).astype('float32')
        self._c = np.zeros((2, 1, 64)).astype('float32')

    def is_speech(self, audio_chunk_int16):
        # Audio debe ser float32 / 32768.0
        # Chunk expectation: 512, 1024, or 1536 samples.
        # We will handle whatever comes, but ideally 512 (32ms).
        
        audio_float32 = audio_chunk_int16.astype(np.float32) / 32768.0
        
        # Add batch dimension: [1, N]
        input_tensor = audio_float32[np.newaxis, :]
        
        # ONNX Inference
        ort_inputs = {
            'input': input_tensor, 
            'sr': np.array([self.sample_rate], dtype=np.int64),
            'h': self._h,
            'c': self._c
        }
        
        out, h, c = self.session.run(None, ort_inputs)
        
        # Update states
        self._h = h
        self._c = c
        
        # Output is probability
        probability = out[0][0]
        return probability > self.threshold, probability
