import numpy as np

from .conversions import euler2euler


class EulerAnglesRelion(np.ndarray):
    def __new__(cls, euler_angles: np.ndarray, source_convention):
        obj = euler2euler(euler_angles, source_convention=source_convention, target_convention='relion').view(cls)
        return obj


class EulerAnglesWarp(np.ndarray):
    def __new__(cls, euler_angles: np.ndarray, source_convention):
        obj = euler2euler(euler_angles, source_convention=source_convention, target_convention='warp').view(cls)
        return obj


class EulerAnglesM(np.ndarray):
    def __new__(cls, euler_angles: np.ndarray, source_convention):
        obj = euler2euler(euler_angles, source_convention=source_convention, target_convention='m').view(cls)
        return obj


class EulerAnglesDynamo(np.ndarray):
    def __new__(cls, euler_angles: np.ndarray, source_convention):
        obj = euler2euler(euler_angles, source_convention=source_convention, target_convention='dynamo').view(cls)
        return obj


class EulerAnglesPeet(np.ndarray):
    def __new__(cls, euler_angles: np.ndarray, source_convention):
        obj = euler2euler(euler_angles, source_convention=source_convention, target_convention='peet').view(cls)
        return obj


class EulerAnglesEmclarity(np.ndarray):
    def __new__(cls, euler_angles: np.ndarray, source_convention):
        obj = euler2euler(euler_angles, source_convention=source_convention, target_convention='emclarity').view(cls)
        return obj
