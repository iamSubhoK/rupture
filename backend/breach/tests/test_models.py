from django.test import TestCase
from breach.models import Target, Victim


class ModelTestCase(TestCase):
    def setUp(self):
        self.target = Target.objects.create(
            endpoint='https://di.uoa.gr/?breach=%s',
            prefix='test',
            alphabet='01'
        )

        self.victim = Victim.objects.create(
            target=self.target,
            sourceip='0.0.0.0'
        )

    def test_target(self):
        self.assertEqual(self.target.host, 'di.uoa.gr')
        self.assertEqual(self.target.port, 443)
        self.assertEqual(self.target.samplesize, 64)
        self.assertEqual(self.target.confidence_threshold, 1.0)
        self.assertEqual(self.target.compression_function_factor, 1.05)
        self.assertEqual(self.target.amplification_factor, 1.05)
        self.assertTrue(self.target.huffman_pool)
        self.assertTrue(self.target.block_align)
        self.assertEqual(self.target.method, 1)

        self.assertEqual(self.target._meta.get_field('sentinel').max_length, 1)
        self.assertTrue(self.target._meta.get_field('name').unique)

    def test_victim(self):
        self.assertEqual(self.victim.interface, 'wlan0')
        self.assertEqual(self.victim.state, 'discovered')
        self.assertEqual(self.victim.realtimeurl, 'http://localhost:3031')
        self.assertEqual(self.victim.snifferendpoint, 'http://127.0.0.1:9000')
        self.assertEqual(self.victim.calibration_wait, 0.0)
