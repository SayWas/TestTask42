<template>
    <div class="login-container">
        <form @submit.prevent="handleLogin">
            <h1>Login</h1>
            <div class="input-group">
                <input type="username" v-model="username" placeholder="Username" required autofocus />
            </div>
            <div class="input-group">
                <input type="password" v-model="password" placeholder="Password" required />
            </div>
            <button type="submit" class="login-button">Log In</button>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore';

const username = ref('');
const password = ref('');
const userStore = useUserStore();
const router = useRouter();

const handleLogin = async () => {
    try {
        await userStore.login(username.value, password.value);
        const redirect = router.currentRoute.value.query.redirect || '/';
        const effectiveRedirect = Array.isArray(redirect) ? redirect[0] : redirect;
        router.push(effectiveRedirect as string);
    } catch (error) {
        console.error('Login failed:', error);
        alert('Login failed! Check credentials.');
    }
};
</script>

<style lang="scss">
@import "../assets/styles/variables.scss";
@import "../assets/styles/mixins.scss";

.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(to right, $primary-color, $secondary-color);
    font-family: $font-family-base;

    form {
        width: 100%;
        max-width: 360px;
        padding: 2rem;
        background-color: rgba(255, 255, 255, 0.92);
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        text-align: center;

        @include transition(all 0.3s ease-in-out);

        &:hover {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
        }

        h1 {
            color: $primary-color;
            margin-bottom: 1.5rem;
        }

        .input-group {
            margin-bottom: 1.5rem;

            input {
                width: 90%;
                padding: 0.8rem;
                font-size: 1rem;
                border: 2px solid transparent;
                border-bottom-color: $input-border-color;
                background: transparent;
                outline: none;

                &:focus {
                    @include transition(border-color 0.3s ease-in-out);
                    border-color: $focus-color;
                }
            }
        }

        .login-button {
            width: 100%;
            padding: 0.8rem;
            font-size: 1rem;
            color: white;
            background-color: $button-background-color;
            border: none;
            border-radius: 8px;
            cursor: pointer;

            &:hover {
                background-color: $hover-color;
                @include transition(background-color 0.3s ease);
            }
        }
    }
}
</style>