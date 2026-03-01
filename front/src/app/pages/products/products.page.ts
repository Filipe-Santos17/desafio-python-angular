import { Component, inject, signal } from "@angular/core";
import { DecimalPipe, DatePipe } from "@angular/common";
import { Router } from '@angular/router';

import type { tDataProduct, tDeleteProductMsg, tEditProductMsg, tCreateProductMsg } from "../../@types";
import { globalFetch } from "../../services/global_fetch";

import { DeleteModalProduct } from "../../components/common/modais/product/delete/delete-modal-product"
import { EditModalProduct } from  "../../components/common/modais/product/edit/edit-modal-product"
import { CreateModalProduct } from  "../../components/common/modais/product/create/create-modal-product"
import { deleteToken } from "../../services/token";


type tProducts = tDataProduct['data']
type tProduct = tProducts[number]
type tEditProduct = Omit<tDataProduct['data'][number], 'created_at' | 'updated_at'>
type tCreateProduct = Omit<tDataProduct['data'][number], 'created_at' | 'updated_at' | 'id'>

@Component({
    selector: "products-page",
    templateUrl: "./products.page.html",
    imports: [DecimalPipe, DatePipe, DeleteModalProduct, EditModalProduct, CreateModalProduct],
})
export class ProductsPage{
    dataTableProducts = signal<tProducts>([])
    selectedProduct = signal<any | null>(null)
    isCreateModalOpen = signal(false)
    isEditModalOpen = signal(false)
    isDeleteModalOpen = signal(false)

    private router = inject(Router);

    ngOnInit() {
        this.loadProducts()
    }

    onLogout = async () => {
        try{
            await globalFetch<any, tDataProduct>("auth-logoff")
            
            deleteToken()
            
            this.router.navigate(['/login']);
        } catch(e){
            console.error(e)
        }
    }

    async loadProducts(){
        try {
            const { data } = await globalFetch<any, tDataProduct>("product-get")

            this.dataTableProducts.set(data.data)
        } catch(e){
            console.error(e)
        }
    }

    onClickBtnCreate(){
        this.isCreateModalOpen.set(true)
    }

    onClickBtnEdit(product: tProduct) {
        this.selectedProduct.set(product)
        this.isEditModalOpen.set(true)
    }

    onClickBtnDelete(id: number) {
        const product = this.dataTableProducts().find(p => p.id === id)
        if (!product) return

        this.selectedProduct.set(product)
        this.isDeleteModalOpen.set(true)
    }

    handleCreate = async (newValueProduct: tCreateProduct) => {
        try{
            await globalFetch<any, tCreateProductMsg>("product-register", newValueProduct)

            this.closeModals()

            setTimeout(() => this.loadProducts(), 2500)
        } catch(e){
            console.error(e)
        }
    }

    handleEdit = async (newValueProduct: tEditProduct) => {
        try{
            const { id } = newValueProduct
            
            await globalFetch<any, tEditProductMsg>("product-change", newValueProduct, {
                specificId: id,
            })

            this.closeModals()
            
            const newProducts = this.dataTableProducts().map(p => {
                if(p.id === id){
                    p.mark = newValueProduct.mark
                    p.name = newValueProduct.name
                    p.value = newValueProduct.value
                    p.updated_at = Date.now().toString()
                }

                return p
            })

            this.dataTableProducts.set(newProducts)
        } catch (e){
            console.error(e)
        }
    }

    handleDelete = async () => {
        try{
            const {id} = this.selectedProduct()
            
            await globalFetch<any, tDeleteProductMsg>("product-remove", null, {
                specificId: id,
            })

            this.closeModals()
            
            const newProducts = this.dataTableProducts().filter(p => p.id !== id)

            this.dataTableProducts.set(newProducts)
        } catch(e){
            console.error(e)
        }
    }

    closeModals() {
        this.isEditModalOpen.set(false)
        this.isDeleteModalOpen.set(false)
        this.isCreateModalOpen.set(false)
        this.selectedProduct.set(null)
    }
}