<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});
Route::namespace('Users')->group(function (){
    Route::get('login', 'LoginController@login_get')->name('login');
    Route::post('login', 'LoginController@login_post')->name('register');
    Route::post('logout', 'LoginController@logout')->name('logout');
    Route::get('register', 'RegisterController@register_get');
    Route::post('register', 'RegisterController@register_post');
});

Route::middleware('auth')->group(function (){
    Route::get('/home', 'HomeController@index')->name('home');
});
