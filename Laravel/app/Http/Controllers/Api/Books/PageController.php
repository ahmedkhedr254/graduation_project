<?php

namespace App\Http\Controllers\Api\Books;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Book;
use App\Page;
use Illuminate\Support\Facades\Validator;

class PageController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        //
        $book_id = \request('id');
        if(isset($book_id)){
            $pages = Book::find($book_id)->pages;
            if (isset($pages)) {
                $count = $pages->count();
                return response(['status' => true, 'count' => $count, 'pages' => $pages]);
            }else{
                return response(['status' => false, 'messages' => 'Book not found']);
            }
        }
        else {
            return response(['status' => false, 'messages' => 'Book not found']);
        }
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
        $book_id = request('id');
        if(isset($book_id)){
            $book = Book::find($book_id);
            if (isset($book)) {
                $validator =  Validator::make(\request()->all(), [
                    'page_number' => ['required', 'integer'],
                    'content' => ['required', 'string', 'max:3999'],
                ]);
                if ($validator->fails()){
                    return response(['status' => false, 'messages' => $validator->messages()]);
                }else {
                    $page = new Page;
                    $page->page_number = request('page_number');
                    $page->content = request('content');
                    $page->book_id = request('id');
                    $page->save();
                    return response(['status' => true, 'page' => $page]);
                }
            }else{
                return response(['status' => false, 'messages' => 'Book not found']);
            }
        }
        else {
            return response(['status' => false, 'messages' => 'ID Not Found']);
        }
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        //
        $page = Page::find($id);
        if(isset($page)) {
            return response(['status' => true, 'page' => $page]);
        }else {
            return response(['status' => false, 'messages' => 'Book not found']);
        }
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
        $page = Page::find($id);
        $book_id = \request('id');
        if(isset($book_id) && isset($page)){
            $book = Book::find($book_id);
            if (isset($book)) {
                $validator =  Validator::make(\request()->all(), [
                    'page_number' => ['required', 'integer'],
                    'content' => ['required', 'string', 'max:3999'],
                ]);
                if ($validator->fails()){
                    return response(['status' => false, 'messages' => $validator->messages()]);
                }else {
                    $page->page_number = request('page_number');
                    $page->content = request('content');
                    $page->book_id = request('id');
                    $page->save();
                    return response(['status' => true, 'page' => $page]);
                }
            }else{
                return response(['status' => false, 'messages' => 'Book not found']);
            }
        }
        else {
            return response(['status' => false, 'messages' => 'Page Not Found']);
        }
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
        $page = Page::find($id);
        if(isset($page)) {
            $page->delete();
            return response(['status' => true, 'messages' => 'Page deleted successfully']);
        }else {
            return response(['status' => false, 'messages' => 'Page not found']);
        }
    }
}
